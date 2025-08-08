from .models import CartItem
def cart_item_count(request):
    """购物车商品数量上下文处理器"""
    if request.user.is_authenticated:
        return {'cart_item_count': CartItem.objects.filter(user=request.user).count()}
    return {'cart_item_count': 0}