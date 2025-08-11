# 导入Django的render函数，用于渲染模板
from django.shortcuts import render
# 导入get_object_or_404函数，用于获取对象或返回404错误
from django.shortcuts import get_object_or_404
# 导入当前应用的模型
from .models import Product, Category


def product_list(request, category_slug=None):
    """商品列表页，支持按分类筛选

    参数:
        request: HTTP请求对象
        category_slug: 分类的URL别名，可选参数

    返回:
        渲染后的商品列表页面
    """
    # 初始化分类变量为None
    category = None
    # 获取所有激活的分类
    categories = Category.objects.filter(is_active=True)
    # 获取所有激活的商品
    products = Product.objects.filter(is_active=True)

    # 如果提供了分类别名，则筛选该分类下的商品
    if category_slug:
        # 获取指定别名的分类，如果不存在则返回404错误
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        # 筛选该分类下的商品
        products = products.filter(category=category)

    # 准备上下文数据
    context = {
        'category': category,       # 当前选中的分类
        'categories': categories,   # 所有激活的分类
        'products': products        # 筛选后的商品列表
    }
    # 渲染模板并返回响应
    return render(request, 'products_list.html', context)


def product_detail(request, id, slug):
    """商品详情页

    参数:
        request: HTTP请求对象
        id: 商品ID
        slug: 商品的URL别名

    返回:
        渲染后的商品详情页面
    """
    # 获取指定ID和别名的商品，如果不存在则返回404错误
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)

    # 准备上下文数据
    context = {
        'product': product  # 当前商品对象
    }
    # 渲染模板并返回响应
    return render(request, 'products_detail.html', context)


def product_search(request):
    """商品搜索功能

    参数:
        request: HTTP请求对象

    返回:
        渲染后的搜索结果页面
    """
    # 从GET请求参数中获取搜索关键词，默认为空字符串
    query = request.GET.get('q', '')

    # 如果有搜索关键词，则按名称模糊搜索
    if query:
        products = Product.objects.filter(
            is_active=True,
            name__icontains=query  # 按商品名称不区分大小写模糊搜索
        )
    # 如果没有搜索关键词，则返回所有激活的商品
    else:
        products = Product.objects.filter(is_active=True)

    # 获取所有激活的分类
    categories = Category.objects.filter(is_active=True)

    # 渲染模板并返回响应
    return render(request, 'products_list.html', {
        'products': products,   # 搜索结果商品列表
        'categories': categories,  # 所有激活的分类
        'query': query          # 搜索关键词
    })