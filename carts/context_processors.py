def cart_item_count(request):
    """购物车商品数量上下文处理器"""
    if request.user.is_authenticated:
        from .models import CartItem
        return {'cart_item_count': CartItem.objects.filter(user=request.user).count()}
    return {'cart_item_count': 0}