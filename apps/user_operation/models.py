# _*_ coding: utf-8 _*_
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from goods.models import Goods

User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏
    """

    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='goods', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'user fav'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name


class UserLeavingMessage(models.Model):
    """
    用户留言
    """

    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '询问'),
        (4, '售后'),
        (5, '求购'),
    )

    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    msg_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES,
                                   help_text='留言类型：1(留言),2(投诉),3(询问),4(售后),5(求购)',
                                   verbose_name='留言类型')
    subject = models.CharField(max_length=100, default='', verbose_name='subject')
    message = models.TextField(default='', verbose_name='留言内容', help_text='留言内容')
    file = models.FileField(upload_to='message/images/', verbose_name='上传的文件', help_text='上传的文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    province = models.CharField(max_length=100, default='', verbose_name='province')
    city = models.CharField(max_length=100, default='', verbose_name='city')
    district = models.CharField(max_length=100, default='', verbose_name='district')
    address = models.CharField(max_length=100, default='', verbose_name='address')
    signer_name = models.CharField(max_length=30, default='', verbose_name='signer name')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='signer mobile')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'User Address'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
