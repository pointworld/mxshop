# _*_ coding: utf-8 _*_

from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

# Create your models here.

User = get_user_model()


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='goods', on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name='bought nums')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'Cart'

    def __str__(self):
        return '%s(%d)'.format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
    订单
    """

    PAY_STATUS = (
        ('success', 'trade success'),
        ('cancel', 'trade cancel'),
        ('paying', 'waiting for paying'),
    )

    PAY_TYPE = (
        ('alipay', 'alipay'),
        ('wechat', 'wechat'),
    )

    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    # 订单唯一编号
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name='order serial number')
    # 支付宝支付时的交易号与本系统订单进行关联
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='trade number')
    # 支付状态
    pay_status = models.CharField(choices=PAY_STATUS, default='paying', max_length=20, verbose_name='pay status')
    # 支付类型
    pay_type = models.CharField(choices=PAY_TYPE, default='alipay', verbose_name='pay type')
    # 订单留言
    order_additional_msg = models.CharField(max_length=200, verbose_name='message left by user')
    # 订单总额
    order_amount = models.FloatField(default=0.0, verbose_name='order amount')
    # 支付时间
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='pay time')

    # 用户地址
    address = models.CharField(max_length=100, default='', verbose_name='to shipping address')
    # 签收者名字
    signer_name = models.CharField(max_length=20, default='', verbose_name='signer name')
    # 签收者电话
    signer_mobile = models.CharField(max_length=11, verbose_name='signer mobile')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'order info'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单的商品详情
    """

    # 一个订单对应多个商品，所以添加外键
    order = models.ForeignKey(OrderInfo, verbose_name='order info', on_delete=models.CASCADE)
    # 两个外键形成一张关联表
    goods = models.ForeignKey(Goods, verbose_name='goods', on_delete=models.CASCADE)
    goods_nums = models.IntegerField(default=0, verbose_name='goods nums')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'order goods'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
