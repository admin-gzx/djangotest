from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify

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
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_final_price(self):
        """获取最终价格(折扣价或原价)"""
        if self.discount_price:
            return self.discount_price
        return self.price