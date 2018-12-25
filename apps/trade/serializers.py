#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

__author__ = 'point'
__date__ = '2018-12-25'

from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart
from goods.serializers import GoodsSerializer


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShoppingCartSerializer(serializers.Serializer):
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

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

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