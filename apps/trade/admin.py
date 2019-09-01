from django.contrib import admin

from .models import Cart, Order, OrderGoods


# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'nums', 'add_time']
    list_filter = ['user', 'goods', 'nums', 'add_time']
    search_fields = ['user', 'goods', 'nums']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_sn', 'trade_no', 'pay_status', 'pay_type', 'leave_msg', 'mount',
                    'add_time']
    list_filter = ['user', 'order_sn', 'trade_no', 'pay_status', 'pay_type', 'leave_msg', 'mount',
                   'add_time']
    search_fields = ['user', 'order_sn', 'trade_no', 'pay_status', 'pay_type', 'leave_msg', 'mount']


class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods', 'goods_nums', 'add_time']
    list_filter = ['order', 'goods', 'goods_nums', 'add_time']
    search_fields = ['order', 'goods', 'goods_nums']


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderGoods, OrderGoodsAdmin)
