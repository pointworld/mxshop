#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

__author__ = 'point'
__date__ = '2018-12-24'

import re

from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from mxshop.settings import REGEXP_MOBILE
from users.models import AuthCode

from rest_framework import serializers

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码（函数名称必须为 validate_ + 字段名）
        :param data:
        :return:
        """
        # 验证手机是否已注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')

        # 验证手机号码是否合法
        if not re.match(REGEXP_MOBILE, mobile):
            raise serializers.ValidationError('手机号码不合法')

        # 验证发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if AuthCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送未超过60s')

        return mobile
