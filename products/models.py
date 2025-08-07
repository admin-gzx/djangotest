from django.db import models
from django.utils.text import slugify
import uuid  # 建议在顶部导入，避免重复导入

class Category(models.Model):
    """商品分类模型"""
    name = models.CharField(max_length=100, verbose_name="分类名称")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL别名")
    description = models.TextField(blank=True, verbose_name="分类描述")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 仅在slug为空时生成（避免更新时重复添加随机字符串）
        if not self.slug or self.slug.strip() == '':
            # 确保基础slug有值（即使名称特殊字符过多）
            base_slug = slugify(self.name) or 'category'
            # 添加随机字符串确保唯一性
            self.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'
        super().save(*args, **kwargs)  # 注意缩进，必须在方法内部


class Product(models.Model):
    """商品模型"""
    name = models.CharField(max_length=200, verbose_name="商品名称")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL别名")
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="所属分类")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="折扣价")
    stock = models.PositiveIntegerField(default=0, verbose_name="库存")
    image = models.ImageField(upload_to='products/', blank=True, verbose_name="商品图片")
    description = models.TextField(verbose_name="商品描述")
    is_featured = models.BooleanField(default=False, verbose_name="是否推荐")
    is_active = models.BooleanField(default=True, verbose_name="是否上架")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or 'product'
            self.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'  # 建议Product也统一用随机字符串确保唯一
        super().save(*args, **kwargs)

    def get_final_price(self):
        """获取最终价格(折扣价或原价)"""
        if self.discount_price:
            return self.discount_price
        return self.price