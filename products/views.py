from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request, category_slug=None):
    """商品列表页，支持按分类筛选"""
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'list.html', context)


def product_detail(request, id, slug):
    """商品详情页"""
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)

    context = {
        'product': product
    }
    return render(request, 'detail.html', context)


def product_search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            is_active=True,
            name__icontains=query  # 按商品名称模糊搜索
        )
    else:
        products = Product.objects.filter(is_active=True)

    categories = Category.objects.filter(is_active=True)
    return render(request, 'list.html', {
        'products': products,
        'categories': categories,
        'query': query
    })