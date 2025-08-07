from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class CartItem(models.Model):
    """购物车项目模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="用户")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "购物车项目"
        verbose_name_plural = "购物车项目"
        unique_together = ('user', 'product')  # 同一用户不能重复添加同一商品

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        """计算小计"""
        return self.quantity * self.product.get_final_price()