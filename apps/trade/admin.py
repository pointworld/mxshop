from django.contrib import admin

from .models import ShoppingCart, OrderInfo, OrderGoods


# Register your models here.


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'nums', 'add_time']
    list_filter = ['user', 'goods', 'nums', 'add_time']
    search_fields = ['user', 'goods', 'nums']


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_sn', 'trade_no', 'pay_status', 'pay_type', 'order_additional_msg', 'order_amount',
                    'add_time']
    list_filter = ['user', 'order_sn', 'trade_no', 'pay_status', 'pay_type', 'order_additional_msg', 'order_amount',
                   'add_time']
    search_fields = ['user', 'order_sn', 'trade_no', 'pay_status', 'pay_type', 'order_additional_msg', 'order_amount']


class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods', 'goods_nums', 'add_time']
    list_filter = ['order', 'goods', 'goods_nums', 'add_time']
    search_fields = ['order', 'goods', 'goods_nums']


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderGoods, OrderGoodsAdmin)
