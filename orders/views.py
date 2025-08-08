from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from carts.models import CartItem
from .models import Order, OrderItem
import logging

logger = logging.getLogger(__name__)

# 表单验证用户输入
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="收件人姓名")
    phone = forms.CharField(max_length=20, label="联系电话")
    address = forms.CharField(widget=forms.Textarea, label="收货地址")

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("请输入有效的电话号码（仅含数字）")
        return phone


@login_required
@transaction.atomic
def checkout(request):
    """结算页面（修复后）"""
    # 加行级锁，防止并发库存问题
    cart_items = CartItem.objects.filter(user=request.user).select_related('product').select_for_update()

    if not cart_items.exists():
        messages.warning(request, '您的购物车是空的')
        return redirect('cart_detail')

    # 检查库存
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f'{item.product.name} 库存不足（当前库存: {item.product.stock}），请减少购买数量'
            )
            return redirect('cart_detail')

    total_price = sum(item.get_total_price() for item in cart_items)
    form = CheckoutForm()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
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

            # 创建订单（依赖视图计算的总金额，而非模型反向计算）
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
                total_price=total_price,  # 直接使用购物车计算的正确金额
                status='pending'
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
                    price=item.product.get_final_price(),
                    quantity=item.quantity
                )

                # 扣减库存
                item.product.stock -= item.quantity
                item.product.save()
                logger.info(
                    f'商品 {item.product.name} 库存更新: {item.product.stock - item.quantity} → {item.product.stock}'
                )

            # 清空购物车
            cart_items.delete()

            messages.success(request, '订单创建成功，请尽快付款')
            return redirect('order_detail', order_id=order.id)

        except IntegrityError as e:
            if "Duplicate entry" in str(e) and "PRIMARY" in str(e):
                # 明确提示自增序列问题
                logger.error(
                    f'订单主键冲突（自增序列异常）: {str(e)}, '
                    f'用户: {request.user.username}'
                )
                messages.error(request, '订单创建失败，请联系管理员重置订单序列')
            else:
                logger.error(f'订单创建失败（完整性错误）: {str(e)}, 用户: {request.user.username}')
                messages.error(request, '创建订单失败，请刷新页面重试')
            return redirect('checkout')
        except Exception as e:
            logger.error(f'订单创建失败: {str(e)}, 用户: {request.user.username}', exc_info=True)
            messages.error(request, '系统错误，请稍后重试')
            return redirect('checkout')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    }
    return render(request, 'orders_checkout.html', context)


# 订单列表和详情视图保持不变（略）
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'orders_detail.html', {'order': order, 'order_items': order_items})