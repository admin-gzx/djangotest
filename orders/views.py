from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from carts.models import CartItem
from .models import Order, OrderItem


@login_required
def checkout(request):
    """结算页面"""
    cart_items = CartItem.objects.filter(user=request.user)

    # 检查购物车是否为空
    if not cart_items.exists():
        messages.warning(request, '您的购物车是空的')
        return redirect('cart_detail')

    # 检查库存
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f'{item.product.name} 库存不足，当前库存: {item.product.stock}')
            return redirect('cart_detail')

    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        # 创建订单
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            total_price=total_price,
            status='pending'
        )

        # 创建订单项目并减少库存
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.get_final_price(),
                quantity=item.quantity
            )

            # 减少库存
            item.product.stock -= item.quantity
            item.product.save()

        # 清空购物车
        cart_items.delete()

        messages.success(request, '订单创建成功，请尽快付款')
        return redirect('order_detail', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'checkout.html', context)


@login_required
def order_list(request):
    """用户订单列表"""
    orders = Order.objects.filter(user=request.user)

    context = {
        'orders': orders
    }
    return render(request, 'list.html', context)


@login_required
def order_detail(request, order_id):
    """订单详情"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order
    }
    return render(request, 'detail.html', context)