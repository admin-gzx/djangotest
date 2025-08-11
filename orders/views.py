from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from carts.models import CartItem
from .models import Order, OrderItem
import logging

logger = logging.getLogger(__name__)

class CheckoutForm(forms.Form):
    """结算表单类
    用于验证用户的收货信息
    """
    # 收件人姓名，最大长度100
    full_name = forms.CharField(max_length=100, label="收件人姓名")
    # 联系电话，最大长度20
    phone = forms.CharField(max_length=20, label="联系电话")
    # 收货地址，使用Textarea小部件允许多行输入
    address = forms.CharField(widget=forms.Textarea, label="收货地址")

    def clean_phone(self):
        """自定义电话号码验证
        确保电话号码只包含数字
        """
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("请输入有效的电话号码（仅含数字）")
        return phone


@login_required
@transaction.atomic
def checkout(request):
    """结算页面视图

    处理用户的订单创建流程，包括库存检查、表单验证、订单创建、
    库存扣减和购物车清空等操作

    参数:
        request: HTTP请求对象

    返回:
        渲染后的结算页面或重定向到其他页面
    """
    # 加行级锁，防止并发库存问题
    # select_related('product')用于提前加载关联的product对象，减少数据库查询
    cart_items = CartItem.objects.filter(user=request.user).select_related('product').select_for_update()

    # 检查购物车是否为空
    if not cart_items.exists():
        messages.warning(request, '您的购物车是空的')
        return redirect('cart_detail')

    # 检查每个商品的库存是否足够
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f'{item.product.name} 库存不足（当前库存: {item.product.stock}），请减少购买数量'
            )
            return redirect('cart_detail')

    # 计算订单总金额
    total_price = sum(item.get_total_price() for item in cart_items)
    # 初始化结算表单
    form = CheckoutForm()

    # 处理POST请求
    if request.method == 'POST':
        # 绑定表单数据
        form = CheckoutForm(request.POST)
        # 验证表单数据
        if not form.is_valid():
            messages.error(request, '请检查提交的信息是否正确')
            return render(request, 'orders_checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'form': form
            })

        try:
            # 获取表单数据
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']

            # 创建订单
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
                total_price=total_price,  # 直接使用购物车计算的正确金额
                status='pending'  # 初始状态为待付款
            )
            logger.info(
                f'用户 {request.user.username} 创建订单 {order.id} 成功，'
                f'总金额: {total_price}, 商品数量: {len(cart_items)}'
            )

            # 创建订单项并扣减库存
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.get_final_price(),  # 使用商品的最终价格（考虑折扣）
                    quantity=item.quantity
                )

                # 扣减库存
                item.product.stock -= item.quantity
                item.product.save()
                logger.info(
                    f'商品 {item.product.name} 库存更新: {item.product.stock + item.quantity} → {item.product.stock}'
                )

            # 清空购物车
            cart_items.delete()

            messages.success(request, '订单创建成功，请尽快付款')
            return redirect('order_detail', order_id=order.id)

        except IntegrityError as e:
            if "Duplicate entry" in str(e) and "PRIMARY" in str(e):
                # 处理主键冲突（自增序列异常）
                logger.error(
                    f'订单主键冲突（自增序列异常）: {str(e)}, '
                    f'用户: {request.user.username}'
                )
                messages.error(request, '订单创建失败，请联系管理员重置订单序列')
            else:
                # 处理其他完整性错误
                logger.error(f'订单创建失败（完整性错误）: {str(e)}, 用户: {request.user.username}')
                messages.error(request, '创建订单失败，请刷新页面重试')
            return redirect('checkout')
        except Exception as e:
            # 处理其他异常
            logger.error(f'订单创建失败: {str(e)}, 用户: {request.user.username}', exc_info=True)
            messages.error(request, '系统错误，请稍后重试')
            return redirect('checkout')

    # 准备上下文数据
    context = {
        'cart_items': cart_items,   # 购物车项列表
        'total_price': total_price,  # 订单总金额
        'form': form                # 结算表单
    }
    # 渲染模板并返回响应
    return render(request, 'orders_checkout.html', context)


@login_required
def order_list(request):
    """订单列表视图

    显示当前登录用户的所有订单

    参数:
        request: HTTP请求对象

    返回:
        渲染后的订单列表页面
    """
    # 获取当前用户的所有订单，按创建时间降序排序
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    # 渲染模板并返回响应
    return render(request, 'orders_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """订单详情视图

    显示指定订单的详细信息和订单项

    参数:
        request: HTTP请求对象
        order_id: 订单ID

    返回:
        渲染后的订单详情页面
    """
    # 获取指定ID的订单，如果不存在则返回404错误
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # 获取该订单的所有订单项
    order_items = OrderItem.objects.filter(order=order)
    # 渲染模板并返回响应
    return render(request, 'orders_detail.html', {'order': order, 'order_items': order_items})