from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import CartItem


@login_required
def cart_detail(request):
    """购物车详情"""
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'carts/detail.html', context)


@login_required
def cart_add(request, product_id):
    """添加商品到购物车"""
    product = get_object_or_404(Product, id=product_id, is_active=True)

    # 检查库存
    if product.stock <= 0:
        messages.error(request, '该商品暂时缺货')
        return redirect('product_detail', id=product.id, slug=product.slug)

    # 尝试获取已存在的购物车项
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    # 如果已存在，则增加数量
    if not created:
        # 检查是否超过库存
        if cart_item.quantity + 1 > product.stock:
            messages.error(request, f'超过库存限制，当前库存: {product.stock}')
        else:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, '商品已添加到购物车')
    else:
        messages.success(request, '商品已添加到购物车')

    return redirect('cart_detail')


@login_required
def cart_update(request, item_id):
    """更新购物车商品数量"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    # 检查库存
    if quantity > cart_item.product.stock:
        messages.error(request, f'超过库存限制，当前库存: {cart_item.product.stock}')
        return redirect('cart_detail')

    if quantity <= 0:
        cart_item.delete()
        messages.success(request, '商品已从购物车移除')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, '购物车已更新')

    return redirect('cart_detail')


@login_required
def cart_remove(request, item_id):
    """从购物车移除商品"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, '商品已从购物车移除')
    return redirect('cart_detail')