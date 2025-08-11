from django.shortcuts import render
from django.db import transaction 
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import CartItem
import logging
logger = logging.getLogger(__name__)

@login_required
def cart_detail(request):
    """购物车详情视图

    显示当前登录用户的购物车内容和总金额

    参数:
        request: HTTP请求对象

    返回:
        渲染后的购物车详情页面
    """
    # 获取当前用户的所有购物车项
    cart_items = CartItem.objects.filter(user=request.user)
    # 计算购物车总金额
    total_price = sum(item.get_total_price() for item in cart_items)

    # 准备上下文数据
    context = {
        'cart_items': cart_items,   # 购物车项列表
        'total_price': total_price  # 购物车总金额
    }
    # 渲染模板并返回响应
    return render(request, 'carts_detail.html', context)




@login_required
@transaction.atomic
def cart_add(request, product_id):
    """添加商品到购物车视图

    将指定商品添加到当前登录用户的购物车
    包含库存检查和事务处理

    参数:
        request: HTTP请求对象
        product_id: 商品ID

    返回:
        重定向到购物车详情页面
    """
    # 获取指定ID的商品，如果不存在或未激活则返回404错误
    product = get_object_or_404(Product, id=product_id, is_active=True)

    # 检查商品库存
    if product.stock <= 0:
        messages.error(request, '该商品暂时缺货')
        return redirect('product_detail', id=product.id, slug=product.slug)

    # 尝试获取已存在的购物车项，如果不存在则创建
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    # 如果购物车项已存在，则增加数量
    if not created:
        # 检查是否超过库存限制
        if cart_item.quantity + 1 > product.stock:
            messages.error(request, f'超过库存限制，当前库存: {product.stock}')
        else:
            # 增加购物车项数量
            cart_item.quantity += 1
            cart_item.save()
            # 减少商品库存
            product.stock -= 1
            product.save()
            messages.success(request, '商品已添加到购物车')
            logger.info(f'用户 {request.user.username} 添加商品 {product.name} 到购物车，库存从 {product.stock+1} 减少到 {product.stock}')
    # 如果是新创建的购物车项
    else:
        # 减少商品库存
        product.stock -= 1
        product.save()
        messages.success(request, '商品已添加到购物车')

    # 重定向到购物车详情页面
    return redirect('cart_detail')




@login_required
@transaction.atomic
def cart_update(request, item_id):
    """更新购物车商品数量视图

    更新当前登录用户购物车中指定商品的数量
    包含库存检查和事务处理

    参数:
        request: HTTP请求对象
        item_id: 购物车项ID

    返回:
        重定向到购物车详情页面
    """
    # 获取指定ID的购物车项，如果不存在则返回404错误
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    # 获取请求中的新数量，默认为1
    quantity = int(request.POST.get('quantity', 1))
    # 记录旧数量
    old_quantity = cart_item.quantity

    # 检查库存是否足够
    # 公式解释: 新数量 <= 现有库存 + (旧数量 - 新数量)
    # 即: 新数量 - (旧数量 - 新数量) <= 现有库存
    # 即: 2*新数量 - 旧数量 <= 现有库存
    if quantity > cart_item.product.stock + (old_quantity - quantity):
        messages.error(request, f'超过库存限制，当前库存: {cart_item.product.stock}')
        return redirect('cart_detail')

    # 如果数量小于等于0，则移除该商品
    if quantity <= 0:
        # 恢复商品库存
        cart_item.product.stock += cart_item.quantity
        cart_item.product.save()
        # 删除购物车项
        cart_item.delete()
        messages.success(request, '商品已从购物车移除')
    # 更新商品数量
    else:
        # 更新库存: 增加 (旧数量 - 新数量) 的库存
        cart_item.product.stock += (old_quantity - quantity)
        cart_item.product.save()
        # 更新购物车项数量
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, '购物车已更新')
        logger.info(f'用户 {request.user.username} 更新商品 {cart_item.product.name} 数量从 {old_quantity} 到 {quantity}，库存从 {cart_item.product.stock - (old_quantity - quantity)} 调整为 {cart_item.product.stock}')

    # 重定向到购物车详情页面
    return redirect('cart_detail')



@login_required
@transaction.atomic
def cart_remove(request, item_id):
    """从购物车移除商品视图

    从当前登录用户的购物车中移除指定商品
    包含库存恢复和事务处理

    参数:
        request: HTTP请求对象
        item_id: 购物车项ID

    返回:
        重定向到购物车详情页面
    """
    # 获取指定ID的购物车项，如果不存在则返回404错误
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    # 恢复商品库存
    cart_item.product.stock += cart_item.quantity
    cart_item.product.save()
    # 删除购物车项
    cart_item.delete()
    messages.success(request, '商品已从购物车移除')
    # 重定向到购物车详情页面
    return redirect('cart_detail')




@login_required
@transaction.atomic
def cart_clear(request):
    """清空购物车视图

    清空当前登录用户的购物车
    包含批量库存恢复和事务处理

    参数:
        request: HTTP请求对象

    返回:
        重定向到购物车详情页面
    """
    # 获取当前用户的所有购物车项
    cart_items = CartItem.objects.filter(user=request.user)
    # 恢复所有商品库存
    for item in cart_items:
        item.product.stock += item.quantity
        item.product.save()
    # 批量删除购物车项
    cart_items.delete()
    messages.success(request, '购物车已清空')
    # 重定向到购物车详情页面
    return redirect('cart_detail')