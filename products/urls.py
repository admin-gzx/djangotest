# 导入Django的path函数，用于定义URL路由
from django.urls import path
# 导入当前应用的视图模块
from . import views

# URL路由配置列表
urlpatterns = [
    # 商品列表页路由
    # 匹配根路径，调用product_list视图函数
    path('', views.product_list, name='product_list'),
    
    # 分类商品列表页路由
    # 匹配带有分类slug的路径，调用product_list视图函数
    # category_slug: 分类的URL别名，用于筛选特定分类的商品
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    
    # 商品详情页路由
    # 匹配带有商品ID和slug的路径，调用product_detail视图函数
    # id: 商品的唯一标识符
    # slug: 商品的URL别名，用于SEO优化
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # 商品搜索路由
    # 匹配搜索路径，调用product_search视图函数
    path('search/', views.product_search, name='product_search'),
]