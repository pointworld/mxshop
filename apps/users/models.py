# _*_ encoding:utf8 _*_

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """

    # 自定义的性别选择规则
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )

    # 用户注册时，需要新建 user_profile，但用户注册时只提供了手机号和密码，没有用户名，所以这里的用户名可以为空
    # 类似的情况有两种处理方式：
    # 1. 设置 null=True, blank=True
    # 2. 设置 default=''

    username = models.CharField(max_length=30, null=True, blank=True, verbose_name='username')
    # 出生日期，年龄可以通过出生日期推算
    birthday = models.DateField(null=True, blank=True, verbose_name='birthday')
    # 性别，只能是男或女，默认女
    gender = models.CharField(
        max_length=10,
        verbose_name='gender',
        choices=GENDER_CHOICES,
        default='female',
    )
    # mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='mobile')
    mobile = models.CharField(max_length=11, verbose_name='mobile')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='email')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class AuthCode(models.Model):
    """
    短信验证码，可以保存在 Redis 中，这里我们直接保存在 MySQL 中
    """

    code = models.CharField(max_length=10, verbose_name='auth code')
    mobile = models.CharField(max_length=11, verbose_name='mobile')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'Auth Code'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code