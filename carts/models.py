# 导入Django模型基类
from django.db import models
# 导入User模型用于关联用户
from django.contrib.auth.models import User
# 导入Product模型用于关联商品
from products.models import Product

class CartItem(models.Model):
    """购物车项目模型
    表示用户购物车中的单个商品项，记录商品、数量和关联用户
    """
    # 用户外键，关联到Django内置的User模型
    # on_delete=models.CASCADE表示当用户被删除时，购物车项目也会被删除
    # null=True, blank=True允许购物车项目不关联用户（例如匿名购物车）
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="用户")
    # 商品外键，关联到Product模型
    # on_delete=models.CASCADE表示当商品被删除时，购物车项目也会被删除
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    # 商品数量，非负整数，默认为1
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    # 创建时间，自动添加
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 更新时间，自动更新
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 模型的单数和复数名称
        verbose_name = "购物车项目"
        verbose_name_plural = "购物车项目"
        # 联合唯一约束，确保同一用户不能重复添加同一商品
        unique_together = ('user', 'product')

    def __str__(self):
        """对象的字符串表示
        返回格式为"数量 x 商品名称"
        """
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        """计算商品项的小计金额
        数量乘以商品的最终价格（考虑折扣）
        """
        return self.quantity * self.product.get_final_price()