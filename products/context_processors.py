def categories(request):
    """分类上下文处理器"""
    from .models import Category
    return {'categories': Category.objects.filter(is_active=True)}