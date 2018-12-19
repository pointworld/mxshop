from django.contrib import admin

from .models import UserProfile, AuthCode


# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'birthday', 'gender', 'mobile', 'email']
    list_filter = ['name', 'birthday', 'gender', 'mobile', 'email']
    search_fields = ['name', 'birthday', 'gender', 'mobile', 'email']


class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'mobile', 'add_time']
    list_filter = ['code', 'mobile', 'add_time']
    search_fields = ['code', 'mobile']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(AuthCode, AuthCodeAdmin)
