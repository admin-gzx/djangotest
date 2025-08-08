from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    """订单模型（修复后）"""
    STATUS_CHOICES = (
        ('pending', '待付款'),
        ('paid', '已付款'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="用户")
    full_name = models.CharField(max_length=100, verbose_name="收件人姓名")
    phone = models.CharField(max_length=20, verbose_name="联系电话")
    address = models.TextField(verbose_name="收货地址")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="订单总金额")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="订单状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"
        ordering = ['-created_at']

    def __str__(self):
        return f"订单 {self.id} - {self.user.username}"

    # 移除原有的 save() 方法！！！
    # 原因：总金额应在创建订单时由视图计算（基于购物车），而非依赖订单项反向计算
    # 若需后续更新总金额（如订单修改），可单独写方法，而非重写 save()


class OrderItem(models.Model):
    """订单项目模型（保持不变）"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="订单")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="购买价格")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")

    class Meta:
        verbose_name = "订单项目"
        verbose_name_plural = "订单项目"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.quantity * self.price