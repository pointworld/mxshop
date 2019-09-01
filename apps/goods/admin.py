from django.contrib import admin

from .models import Goods, Category, CategoryBrand, DetailSlide, IndexSlide, IndexGoodsAd


# Register your models here.


class GoodsAdmin(admin.ModelAdmin):
    list_filter = ['category', 'name', 'sn', 'brief', 'desc', 'hit_nums', 'fav_nums', 'stock_nums', 'sold_nums',
                   'market_price', 'shop_price', 'freight_free', 'cover', 'is_new', 'is_hot', 'add_time']
    list_display = ['category', 'name', 'sn', 'brief', 'desc', 'hit_nums', 'fav_nums', 'stock_nums', 'sold_nums',
                    'market_price', 'shop_price', 'freight_free', 'cover', 'is_new', 'is_hot', 'add_time']
    search_fields = ['category', 'name', 'sn', 'brief', 'desc', 'hit_nums', 'fav_nums', 'stock_nums', 'sold_nums',
                     'market_price', 'shop_price', 'freight_free', 'cover', 'is_new', 'is_hot']


class GoodsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'desc', 'level', 'pid', 'is_tab', 'add_time']
    list_filter = ['name', 'code', 'desc', 'level', 'pid', 'is_tab', 'add_time']
    search_fields = ['name', 'code', 'desc', 'level', 'pid', 'is_tab']


class CategoryBrandAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'desc', 'image', 'add_time']
    list_filter = ['category', 'name', 'desc', 'image', 'add_time']
    search_fields = ['category', 'name', 'desc', 'image']


class DetailSlideAdmin(admin.ModelAdmin):
    list_display = ['goods', 'image', 'add_time']
    list_filter = ['goods', 'image', 'add_time']
    search_fields = ['goods', 'image']


class IndexSlideAdmin(admin.ModelAdmin):
    list_display = ['goods', 'image', 'index', 'add_time']
    list_filter = ['goods', 'image', 'index', 'add_time']
    search_fields = ['goods', 'image', 'index']


class IndexGoodsAdAdmin(admin.ModelAdmin):
    list_display = ['category', 'goods']
    list_filter = ['category', 'goods']
    search_fields = ['category', 'goods']


admin.site.register(Goods, GoodsAdmin)
admin.site.register(Category, GoodsCategoryAdmin)
admin.site.register(CategoryBrand, CategoryBrandAdmin)
admin.site.register(DetailSlide, DetailSlideAdmin)
admin.site.register(IndexSlide, IndexSlideAdmin)
admin.site.register(IndexGoodsAd, IndexGoodsAdAdmin)
