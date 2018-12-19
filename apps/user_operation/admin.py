from django.contrib import admin

from .models import UserFav, UserLeavingMessage, UserAddress


# Register your models here.


class UserFavAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'add_time']
    list_filter = ['user', 'goods', 'add_time']
    search_fields = ['user', 'goods']


class UserLeavingMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'msg_type', 'subject', 'message', 'file', 'add_time']
    list_filter = ['user', 'msg_type', 'subject', 'message', 'file', 'add_time']
    search_fields = ['user', 'msg_type', 'subject', 'message', 'file']


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile', 'add_time']
    list_filter = ['user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile', 'add_time']
    search_fields = ['user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile']


admin.site.register(UserFav, UserFavAdmin)
admin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
