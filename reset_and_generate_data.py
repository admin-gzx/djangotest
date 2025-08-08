import os
import sys
from django.core.management import call_command

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_auth_system.settings')
import django
django.setup()

# 导入模型
from django.contrib.auth.models import User
from products.models import Category, Product
from carts.models import CartItem
from orders.models import Order, OrderItem

# 导入数据生成函数
from generate_test_data import generate_categories, generate_products, generate_users, generate_cart_items, generate_orders

def clear_database():
    """删除数据库中的所有内容"""
    print('正在清除数据库...')
    
    # 删除所有模型的数据
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    CartItem.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    User.objects.all().delete()
    
    print('数据库已清除!')

def main():
    # 清除数据库
    clear_database()
    
    # 重新生成测试数据
    print('开始重新生成测试数据...')
    categories = generate_categories(10)
    products = generate_products(categories, 50)
    users = generate_users(10)
    generate_cart_items(users, products, 30)
    generate_orders(users, products, 20)
    print('测试数据重新生成完成!')

if __name__ == '__main__':
    main()