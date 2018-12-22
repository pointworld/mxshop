# _*_ coding: utf-8 _*_

from datetime import datetime

from django.db import models

# Create your models here.


class GoodsCategory(models.Model):
    """
    商品多级类别
    """

    CATEGORY_TYPE = (
        (1, 'first'),
        (2, 'second'),
        (3, 'third'),
    )

    # help_text: 生成接口测试文档时会用到的
    # related_name: 在后面进行查询的时候会用到

    # 商品类别名
    name = models.CharField(max_length=30, default='', verbose_name='category name', help_text='category name')
    # 商品类别编码，code 不能是中文，可以用于查找
    code = models.CharField(max_length=30, default='', verbose_name='category code', help_text='category code')
    # 商品类别描述
    desc = models.TextField(default='', verbose_name='category description', help_text='category description')
    # 类的级别
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='category type', help_text='category type')
    # 类的父类
    parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='parent category',
                                        on_delete=models.CASCADE, help_text='parent category', related_name='sub_cat')
    # 是否放到 tab 栏
    is_tab = models.BooleanField(default=False, verbose_name='is tab', help_text='is tab')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'goods category'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    某一大类下的宣传商标
    商品的某一个类下又会有多个宣传的商标
    """

    category = models.ForeignKey(GoodsCategory, related_name='brands', null=True, blank=True,
                                 verbose_name='goods category', on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=30, verbose_name='brand name', help_text='brand name')
    desc = models.TextField(default='', max_length=200, verbose_name='brand description', help_text='brand description')
    image = models.ImageField(upload_to='brands/', max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'brands'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """

    # 外键：商品的类别
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE,
                                 verbose_name='category')
    # 默认生成的 id 是数据库做关联，查询用的，但是实际商品还有自己的 sn 码
    sn = models.CharField(max_length=50, default='', verbose_name='serial number')
    name = models.CharField(max_length=100, verbose_name='name', help_text='name')
    brief = models.TextField(max_length=500, verbose_name='brief')
    desc = models.TextField(max_length=2000, verbose_name='desc')
    # desc = UEditorField(imagePath='goods/images/', filePath='goods/images/', width=1000, height=300,
    #                     verbose_name='description', help_text='description')
    hit_nums = models.IntegerField(default=0, verbose_name='hit nums')
    fav_nums = models.IntegerField(default=0, verbose_name='fav nums')
    stock_nums = models.IntegerField(default=0, verbose_name='stock nums')
    sold_nums = models.IntegerField(default=0, verbose_name='sold nums')
    market_price = models.FloatField(default=0, verbose_name='market price')
    shop_price = models.FloatField(default=0, verbose_name='shop price')
    freight_free = models.BooleanField(default=True, verbose_name='is need freight fee')
    cover = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name='cover')
    is_new = models.IntegerField(default=False, verbose_name='is new')
    is_hot = models.IntegerField(default=False, verbose_name='is hot')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'goods'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品详情页轮播图
    """

    goods = models.ForeignKey(Goods, verbose_name='goods', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', verbose_name='detail image', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'goods image'
        # verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    首页轮播的商品图，适配首页大图
    """

    goods = models.ForeignKey(Goods, verbose_name='goods', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name='banner image')
    index = models.IntegerField(default=0, verbose_name='banner index')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'banner goods'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
