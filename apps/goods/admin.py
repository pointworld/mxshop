from django.contrib import admin

from .models import Goods, GoodsCategory, GoodsCategoryBrand, GoodsImage, Banner, IndexGoodsAd


# Register your models here.


class GoodsAdmin(admin.ModelAdmin):
    list_filter = ['category', 'name', 'sn', 'brief', 'desc', 'hit_nums', 'fav_nums', 'stock_nums', 'sold_nums',
                   'market_price', 'shop_price', 'freight_free', 'cover', 'is_new', 'is_hot', 'add_time']
    list_display = ['category', 'name', 'sn', 'brief', 'desc', 'hit_nums', 'fav_nums', 'stock_nums', 'sold_nums',
                    'market_price', 'shop_price', 'freight_free', 'cover', 'is_new', 'is_hot', 'add_time']
    search_fields = ['category', 'name', 'sn', 'brief', 'desc', 'hit_nums', 'fav_nums', 'stock_nums', 'sold_nums',
                     'market_price', 'shop_price', 'freight_free', 'cover', 'is_new', 'is_hot']


class GoodsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'desc', 'category_type', 'parent_category', 'is_tab', 'add_time']
    list_filter = ['name', 'code', 'desc', 'category_type', 'parent_category', 'is_tab', 'add_time']
    search_fields = ['name', 'code', 'desc', 'category_type', 'parent_category', 'is_tab']


class GoodsCategoryBrandAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'desc', 'image', 'add_time']
    list_filter = ['category', 'name', 'desc', 'image', 'add_time']
    search_fields = ['category', 'name', 'desc', 'image']


class GoodsImageAdmin(admin.ModelAdmin):
    list_display = ['goods', 'image', 'add_time']
    list_filter = ['goods', 'image', 'add_time']
    search_fields = ['goods', 'image']


class BannerAdmin(admin.ModelAdmin):
    list_display = ['goods', 'image', 'index', 'add_time']
    list_filter = ['goods', 'image', 'index', 'add_time']
    search_fields = ['goods', 'image', 'index']


class IndexGoodsAdAdmin(admin.ModelAdmin):
    list_display = ['category', 'goods']
    list_filter = ['category', 'goods']
    search_fields = ['category', 'goods']


admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsCategory, GoodsCategoryAdmin)
admin.site.register(GoodsCategoryBrand, GoodsCategoryBrandAdmin)
admin.site.register(GoodsImage, GoodsImageAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(IndexGoodsAd, IndexGoodsAdAdmin)
