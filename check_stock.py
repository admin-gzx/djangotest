import os
import sys

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_auth_system.settings')
import django

django.setup()

from products.models import Product
from carts.models import CartItem
from django.contrib.auth.models import User

# 获取所有用户
users = User.objects.all()

for user in users:
    print(f"\n检查用户 {user.username} 的购物车:")
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items:
        print("  购物车为空")
        continue

    for item in cart_items:
        product = item.product
        print(f"  商品: {product.name}")
        print(f"  购物车数量: {item.quantity}")
        print(f"  当前库存: {product.stock}")

        if item.quantity > product.stock:
            print(f"  警告: 购物车数量超过库存!")
            # 可选：自动修复
            # product.stock += item.quantity
            # product.save()
            # print(f"  已自动修复库存: {product.stock}")

print("\n库存检查完成!")