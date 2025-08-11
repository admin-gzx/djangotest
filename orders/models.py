# 导入Django模型基类
from django.db import models
# 导入User模型用于关联用户
from django.contrib.auth.models import User
# 导入Product模型用于关联商品
from products.models import Product

class Order(models.Model):
    """订单模型
    存储订单的基本信息，包括用户、收货信息、总金额和订单状态等
    """
    # 订单状态选择项
    STATUS_CHOICES = (
        ('pending', '待付款'),
        ('paid', '已付款'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消'),
    )

    # 用户外键，关联到Django内置的User模型
    # related_name='orders'表示在User中可以通过orders访问相关的Order
    # on_delete=models.CASCADE表示当用户被删除时，订单也会被删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="用户")
    # 收件人姓名
    full_name = models.CharField(max_length=100, verbose_name="收件人姓名")
    # 联系电话
    phone = models.CharField(max_length=20, verbose_name="联系电话")
    # 收货地址
    address = models.TextField(verbose_name="收货地址")
    # 订单总金额
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="订单总金额")
    # 订单状态，默认为'pending'(待付款)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="订单状态")
    # 创建时间，自动添加
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 更新时间，自动更新
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 模型的单数和复数名称
        verbose_name = "订单"
        verbose_name_plural = "订单"
        # 按创建时间降序排序（最新的订单在前）
        ordering = ['-created_at']

    def __str__(self):
        """对象的字符串表示
        返回格式为"订单 ID - 用户名"
        """
        return f"订单 {self.id} - {self.user.username}"

    # 注意：移除了原有的 save() 方法
    # 原因：总金额应在创建订单时由视图计算（基于购物车），而非依赖订单项反向计算
    # 若需后续更新总金额（如订单修改），可单独实现方法，而非重写 save()


class OrderItem(models.Model):
    """订单项目模型
    表示订单中的单个商品项，记录商品、购买价格、数量等信息
    """
    # 订单外键，关联到Order模型
    # related_name='items'表示在Order中可以通过items访问相关的OrderItem
    # on_delete=models.CASCADE表示当订单被删除时，订单项目也会被删除
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="订单")
    # 商品外键，关联到Product模型
    # on_delete=models.CASCADE表示当商品被删除时，订单项目也会被删除
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    # 购买价格，记录下单时的价格
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="购买价格")
    # 商品数量，非负整数，默认为1
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")

    class Meta:
        # 模型的单数和复数名称
        verbose_name = "订单项目"
        verbose_name_plural = "订单项目"

    def __str__(self):
        """对象的字符串表示
        返回格式为"数量 x 商品名称"
        """
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        """计算订单项目的小计金额
        数量乘以购买价格
        """
        return self.quantity * self.price