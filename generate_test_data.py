import os
import sys
import random
from faker import Faker

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_auth_system.settings')
import django
django.setup()

# 导入模型
from django.contrib.auth.models import User
from products.models import Category, Product
from carts.models import CartItem
from orders.models import Order, OrderItem

# 初始化Faker
fake = Faker('zh_CN')

# 生成分类数据
def generate_categories(count=10):
    categories = []
    existing_names = set()  # 用于跟踪已生成的名称
    while len(categories) < count:
        name = fake.word(ext_word_list=None)+ fake.random_letter()
        # 确保名称唯一
        if name not in existing_names:
            existing_names.add(name)
            category = Category(
                name=name,
                description=fake.text(max_nb_chars=200),
                is_active=True
            )
            category.save()
            categories.append(category)
    print(f'已生成 {len(categories)} 个分类')
    return categories


# 生成商品数据
def generate_products(categories, count=50):
    products = []
    for _ in range(count):
        category = random.choice(categories)
        name = fake.word(ext_word_list=None) + ' ' + fake.word(ext_word_list=None)
        price = round(random.uniform(10, 1000), 2)
        discount_price = round(price * random.uniform(0.7, 0.95), 2) if random.random() > 0.5 else None
        product = Product(
            name=name,
            category=category,
            price=price,
            discount_price=discount_price,
            stock=random.randint(0, 100),
            description=fake.text(max_nb_chars=500),
            is_featured=random.random() > 0.7,
            is_active=True
        )
        product.save()
        products.append(product)
    print(f'已生成 {len(products)} 个商品')
    return products

# 生成用户数据
def generate_users(count=10):
    users = []
    # # 创建超级用户
    # superuser = User.objects.create_superuser(
    #     username='admin',
    #     email='admin@example.com',
    #     password='admin123'
    # )
    # users.append(superuser)
    # print('已生成超级用户: admin/admin123')

    # 创建普通用户
    for i in range(count):
        username = fake.user_name()
        email = fake.email()
        user = User.objects.create_user(
            username=username,
            email=email,
            password='password123'
        )
        users.append(user)
    print(f'已生成 {len(users)-1} 个普通用户')
    return users

# 生成购物车数据
def generate_cart_items(users, products, count=30):
    cart_items = []
    for _ in range(count):
        user = random.choice(users)
        product = random.choice(products)
        # 确保库存足够
        if product.stock > 0:
            quantity = random.randint(1, min(5, product.stock))
            try:
                # 检查是否已存在该商品的购物车项
                cart_item = CartItem.objects.get(user=user, product=product)
                cart_item.quantity = quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem(
                    user=user,
                    product=product,
                    quantity=quantity
                )
                cart_item.save()
            cart_items.append(cart_item)
    print(f'已生成 {len(cart_items)} 个购物车项目')
    return cart_items

# 生成订单数据
def generate_orders(users, products, count=20):
    orders = []
    for _ in range(count):
        user = random.choice(users)
        # 创建订单
        order = Order(
            user=user,
            full_name=fake.name(),
            phone=fake.phone_number(),
            address=fake.address(),
            total_price=0,
            status=random.choice(['pending', 'paid', 'shipped', 'delivered', 'cancelled'])
        )
        order.save()

        # 添加订单项
        items_count = random.randint(1, 5)
        total_price = 0
        for _ in range(items_count):
            product = random.choice(products)
            if product.stock > 0:
                quantity = random.randint(1, min(3, product.stock))
                price = product.get_final_price()
                order_item = OrderItem(
                    order=order,
                    product=product,
                    price=price,
                    quantity=quantity
                )
                order_item.save()
                total_price += order_item.get_total_price()

        # 更新订单总金额
        order.total_price = total_price
        order.save()
        orders.append(order)
    print(f'已生成 {len(orders)} 个订单')
    return orders

# 主函数
def main():
    print('开始生成测试数据...')
    categories = generate_categories(10)
    products = generate_products(categories, 50)
    users = generate_users(10)
    generate_cart_items(users, products, 30)
    generate_orders(users, products, 20)
    print('测试数据生成完成!')

if __name__ == '__main__':
    main()