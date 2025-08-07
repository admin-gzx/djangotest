import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_auth_system.settings')
django.setup()

from products.models import Product
from carts.models import CartItem
from django.db.models import Sum

# 1. 检查所有商品的库存
print("检查商品库存...")
all_products = Product.objects.all()
for product in all_products:
    # 计算该商品在所有购物车中的总数量
    cart_quantity = CartItem.objects.filter(product=product).aggregate(Sum('quantity'))['quantity__sum'] or 0

    # 如果购物车中的数量大于库存，调整库存
    if cart_quantity > product.stock:
        print(f"调整商品 '{product.name}' 的库存: 原库存 {product.stock}, 购物车总数量 {cart_quantity}")
        product.stock = cart_quantity
        product.save()
        print(f"已将 '{product.name}' 的库存更新为 {product.stock}")
    elif product.stock < 0:
        print(f"修复商品 '{product.name}' 的负库存: {product.stock}")
        product.stock = 0
        product.save()
        print(f"已将 '{product.name}' 的库存设置为 0")
    else:
        print(f"商品 '{product.name}' 库存正常: {product.stock}, 购物车总数量 {cart_quantity}")

# 2. 检查购物车项是否超过库存
print("\n检查购物车项是否超过库存...")
all_cart_items = CartItem.objects.all()
for item in all_cart_items:
    if item.quantity > item.product.stock:
        print(f"购物车项 '{item.product.name}' 数量 {item.quantity} 超过库存 {item.product.stock}")
        # 调整购物车数量
        item.quantity = item.product.stock
        item.save()
        print(f"已将 '{item.product.name}' 的购物车数量调整为 {item.product.stock}")
    else:
        print(f"购物车项 '{item.product.name}' 数量 {item.quantity} 正常")

print("\n库存检查和修复完成！")