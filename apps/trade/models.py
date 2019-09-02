from datetime import datetime

from django.db import models

from goods.models import Goods

# get_user_model 方法会去 settings 中找 AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()


class Cart(models.Model):
    """
    购物车
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    nums = models.IntegerField(default=0, verbose_name='购买数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')

    def __str__(self):
        return '%s(%d)'.format(self.goods.name, self.nums)


class Order(models.Model):
    """
    订单信息
    """

    PAY_STATUS = (
        ('WAIT_BUYER_PAY', '交易创建'),
        ('TRADE_SUCCESS', '支付成功'),
        ('TRADE_FINISHED', '交易完成'),
        ('TRADE_CLOSED', '交易关闭'),
        ('paying', '待支付'),
    )

    PAY_TYPE = (
        ('alipay', '支付宝'),
        ('wechat', '微信'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name='订单唯一编号')
    # 支付宝支付时的交易号与本系统订单进行关联
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付宝交易号')
    # 微信支付会用到
    nonce_str = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name="随机加密串")
    pay_status = models.CharField(choices=PAY_STATUS, default='paying', max_length=20, verbose_name='支付状态')
    pay_type = models.CharField(max_length=20, choices=PAY_TYPE, default='alipay', verbose_name='支付类型')
    leave_msg = models.CharField(max_length=200, verbose_name='订单留言')
    order_amount = models.FloatField(default=0.0, verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    # 用户信息
    address = models.CharField(max_length=100, default='', verbose_name='收货人地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, verbose_name='签收者电话')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单内的商品详情
    """

    # 一个订单对应多个商品
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='goods', verbose_name='订单信息')
    # 两个外键形成一张关联表
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    goods_nums = models.IntegerField(default=0, verbose_name='商品数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
