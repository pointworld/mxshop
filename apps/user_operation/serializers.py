#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

__author__ = 'point'
__date__ = '2018-12-25'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已经收藏'
            )
        ]

        fields = ('user', 'goods', 'id')


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('id', 'user', 'msg_type', 'subject', 'message', 'file', 'add_time')
