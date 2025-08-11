# 导入Django模型基类
from django.db import models
# 导入slugify函数用于生成URL友好的字符串
from django.utils.text import slugify
# 导入uuid模块用于生成唯一标识符
import uuid

class Category(models.Model):
    """商品分类模型
    用于对商品进行分类管理
    """
    # 分类名称，最大长度100
    name = models.CharField(max_length=100, verbose_name="分类名称")
    # URL别名，用于生成友好的URL，确保唯一性
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL别名")
    # 分类描述，可以为空
    description = models.TextField(blank=True, verbose_name="分类描述")
    # 分类是否激活，默认为True
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    # 创建时间，自动添加
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 更新时间，自动更新
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 模型的单数和复数名称
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"
        # 按名称排序
        ordering = ['name']

    def __str__(self):
        """对象的字符串表示"""
        return self.name

    def save(self, *args, **kwargs):
        """重写save方法，在slug为空时自动生成唯一slug"""
        # 仅在slug为空时生成（避免更新时重复添加随机字符串）
        if not self.slug or self.slug.strip() == '':
            # 确保基础slug有值（即使名称特殊字符过多）
            base_slug = slugify(self.name) or 'category'
            # 添加随机字符串确保唯一性
            self.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'
        # 调用父类的save方法
        super().save(*args, **kwargs)


class Product(models.Model):
    """商品模型
    存储商品的详细信息
    """
    # 商品名称，最大长度200
    name = models.CharField(max_length=200, verbose_name="商品名称")
    # URL别名，用于生成友好的URL，确保唯一性
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL别名")
    # 所属分类，外键关联到Category模型
    # related_name='products'表示在Category中可以通过products访问相关的Product
    # on_delete=models.CASCADE表示当分类被删除时，相关商品也会被删除
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="所属分类")
    # 商品价格，最大10位数字，2位小数
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    # 折扣价，可以为空
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="折扣价")
    # 商品库存，非负整数
    stock = models.PositiveIntegerField(default=0, verbose_name="库存")
    # 商品图片，上传到products/目录，可以为空
    image = models.ImageField(upload_to='products/', blank=True, verbose_name="商品图片")
    # 商品描述
    description = models.TextField(verbose_name="商品描述")
    # 是否推荐商品，默认为False
    is_featured = models.BooleanField(default=False, verbose_name="是否推荐")
    # 是否上架，默认为True
    is_active = models.BooleanField(default=True, verbose_name="是否上架")
    # 创建时间，自动添加
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 更新时间，自动更新
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 模型的单数和复数名称
        verbose_name = "商品"
        verbose_name_plural = "商品"
        # 按创建时间降序排序（最新的商品在前）
        ordering = ['-created_at']

    def __str__(self):
        """对象的字符串表示"""
        return self.name

    def save(self, *args, **kwargs):
        """重写save方法，在slug为空时自动生成唯一slug"""
        if not self.slug:
            base_slug = slugify(self.name) or 'product'
            # 添加随机字符串确保唯一性
            self.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'
        # 调用父类的save方法
        super().save(*args, **kwargs)

    def get_final_price(self):
        """获取最终价格(折扣价或原价)
        如果有折扣价，则返回折扣价，否则返回原价
        """
        if self.discount_price:
            return self.discount_price
        return self.price