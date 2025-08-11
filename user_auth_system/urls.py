# 导入Django管理后台
from django.contrib import admin
# 导入render函数用于渲染模板
from django.shortcuts import render
# 导入path和include函数用于URL路由配置
from django.urls import path, include
# 导入settings以访问项目配置
from django.conf import settings
# 导入static函数用于提供静态文件和媒体文件
from django.conf.urls.static import static
# 导入TemplateView用于创建基于模板的简单视图
from django.views.generic import TemplateView

def home(request):
    """商城首页视图
    展示推荐商品和分类导航
    """
    # 延迟导入模型以避免循环引用问题
    from products.models import Product, Category
    # 获取激活状态的推荐商品，最多8个
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    # 获取所有激活状态的分类
    categories = Category.objects.filter(is_active=True)
    # 渲染首页模板并传递数据
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'categories': categories
    })

# URL路由配置列表
urlpatterns = [
    # 管理后台URL
    path('admin/', admin.site.urls),
    # 商城首页URL，name参数用于在模板和视图中引用
    path('', home, name='home'),
    # 用户认证相关URL，包含在accounts应用中
    path('accounts/', include('accounts.urls')),
    # 商品相关URL，包含在products应用中
    path('products/', include('products.urls')),
    # 购物车相关URL，包含在carts应用中
    path('cart/', include('carts.urls')),
    # 订单相关URL，包含在orders应用中
    path('orders/', include('orders.urls')),
]

# 开发环境下提供媒体文件访问
# 在生产环境中，媒体文件应由Web服务器(如Nginx)直接提供
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 开发环境下也可以配置静态文件的提供方式
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)