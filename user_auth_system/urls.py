from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

def home(request):
    """商城首页视图"""
    from products.models import Product, Category
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    categories = Category.objects.filter(is_active=True)
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'categories': categories
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # 商城首页
    path('accounts/', include('accounts.urls')),  # 用户认证
    path('products/', include('products.urls')),  # 商品
    path('cart/', include('carts.urls')),  # 购物车
    path('orders/', include('orders.urls')),  # 订单
]

# 开发环境下提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)