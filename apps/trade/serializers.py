#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import time
from random import Random

from utils.alipay import AliPay

__author__ = 'point'
__date__ = '2018-12-25'

from rest_framework import serializers

from goods.models import Goods
from .models import Cart, Order, OrderGoods
from goods.serializers import GoodsSerializer
from mxshop.settings import ALIPAY_PUB_KEY_PATH, PRIVATE_KEY_PATH


class CartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = Cart
        fields = '__all__'


class CartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, label='数量',
                                    error_messages={
                                        'min_value': '商品数量不能小于1',
                                        'required': '请选择购买数量'
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = Cart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = Cart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        """
        修改商品数量
        :param instance:
        :param validated_data:
        :return:
        """
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            # appid 在沙箱环境中就可以找到
            appid="2016092300575055",
            # 这个值先不管，在与 vue 的联调中介绍
            app_notify_url="http://132.232.184.182:8000/alipay/return/",
            # 我们自己商户的密钥
            app_private_key_path=PRIVATE_KEY_PATH,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_path=ALIPAY_PUB_KEY_PATH,
            # 先不用管，后面 vue 解释
            return_url="http://132.232.184.182:8000/alipay/return/",
            # debug 为 true 时使用沙箱的 url。如果不是则用正式环境的 url，默认 False
            debug=True,
        )

        # 直接支付:生成请求的字符串。
        url = alipay.direct_pay(
            # 订单标题
            subject=obj.order_sn,
            # 我们商户自行生成的订单号
            out_trade_no=obj.order_sn,
            # 订单金额
            total_amount=obj.mount,
        )
        # 将生成的请求字符串拿到我们的url中进行拼接
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = Order
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            # appid 在沙箱环境中就可以找到
            appid="2016092300575055",
            # 这个值先不管，在与 vue 的联调中介绍
            app_notify_url="http://132.232.184.182:8000/alipay/return/",
            # 我们自己商户的密钥
            app_private_key_path=PRIVATE_KEY_PATH,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_path=ALIPAY_PUB_KEY_PATH,
            # 先不用管，后面 vue 解释
            return_url="http://132.232.184.182:8000/alipay/return/",
            # debug 为 true 时使用沙箱的 url。如果不是则用正式环境的 url，默认 False
            debug=True,
        )

        # 直接支付:生成请求的字符串。
        url = alipay.direct_pay(
            # 订单标题
            subject=obj.order_sn,
            # 我们商户自行生成的订单号
            out_trade_no=obj.order_sn,
            # 订单金额
            total_amount=obj.mount,
        )
        # 将生成的请求字符串拿到我们的url中进行拼接
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    def generate_order_sn(self):
        # 当前时间 + userID + 随机数
        order_sn = '{time_str}{user_id}{random_str}'.format(
            time_str=time.strftime('%Y%m%d%H%M%S'),
            user_id=self.context['request'].user.id,
            random_str=Random().randint(10, 99)
        )
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = Order
        fields = '__all__'
