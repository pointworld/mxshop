from datetime import datetime

from django.db import models
from froala_editor.fields import FroalaField


class GoodsCategory(models.Model):
    """
    商品分类
    """

    CATEGORY_TYPE = (
        (1, '一级类目'),
        (2, '二级类目'),
        (3, '三级类目'),
    )

    # help_text: 生成接口测试文档时会用到的
    # related_name: 在后面进行查询的时候会用到

    name = models.CharField(max_length=30, default='', verbose_name='类别名', help_text='类别名')
    code = models.CharField(max_length=30, default='', verbose_name='类别 code', help_text='类别 code')
    desc = models.TextField(default='', verbose_name='类别描述', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别', help_text='类目级别')
    parent_category = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='sub_cat',
        verbose_name='父类别',
        help_text='父类别')
    # 是否放到 tab 栏
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    某一大类下的宣传商标
    商品的某一个类下又会有多个宣传的商标
    """

    category = models.ForeignKey(GoodsCategory, related_name='brands', null=True, blank=True,
                                 on_delete=models.CASCADE, verbose_name='商品类目')
    name = models.CharField(default='', max_length=30, verbose_name='品牌名', help_text='品牌名')
    desc = models.TextField(default='', max_length=200, verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(upload_to='brands/', max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '宣传品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """

    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品类目')
    # 默认生成的 id 是数据库做关联，查询用的，但是实际商品还有自己的 sn 码（serial number）
    sn = models.CharField(max_length=50, default='', verbose_name='商品唯一货号')
    name = models.CharField(max_length=100, verbose_name='商品名', help_text='商品名')
    brief = models.TextField(max_length=500, verbose_name='商品简介')
    desc = FroalaField()
    # desc = models.TextField(max_length=2000, verbose_name='商品描述')
    # desc = UEditorField(imagePath='goods/images/', filePath='goods/images/', width=1000, height=300,
    #                     verbose_name='description', help_text='description')
    hit_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    stock_nums = models.IntegerField(default=0, verbose_name='库存数')
    sold_nums = models.IntegerField(default=0, verbose_name='销售量')
    market_price = models.FloatField(default=0, verbose_name='市场价格')
    shop_price = models.FloatField(default=0, verbose_name='本店价格')
    freight_free = models.BooleanField(default=True, verbose_name='是否免运费')
    # 首页中展示的商品封面图
    cover = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name='封面图')
    # 首页中新品展示
    is_new = models.IntegerField(default=False, verbose_name='是否新品')
    # 商品详情页的热卖商品
    is_hot = models.IntegerField(default=False, verbose_name='是否热销')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexGoodsAd(models.Model):
    """
    商品广告
    """

    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品类目')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')

    class Meta:
        verbose_name = '首页商品类别广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class GoodsImage(models.Model):
    """
    商品详情页轮播图
    """

    goods = models.ForeignKey(Goods, related_name='images', on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(upload_to='', null=True, blank=True, verbose_name='图片')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    首页轮播的商品图，适配首页大图
    因为首页的商品轮播图片是大图，跟商品详情里面的图片不一样，所以要单独写一个首页轮播图 model
    """

    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='轮播图')
    index = models.IntegerField(default=0, verbose_name='轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    搜索栏下方热搜词
    """

    keywords = models.CharField("热搜词", default="", max_length=20)
    index = models.IntegerField("排序", default=0)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = '热搜排行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
