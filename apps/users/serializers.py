import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import AuthCode

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
        if not re.match(settings.REGEXP_MOBILE, mobile):
            raise serializers.ValidationError('手机号码不合法')

        # 验证发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if AuthCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送未超过60s')

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """

    class Meta:
        model = User
        fields = ('name', 'gender', 'birthday', 'email', 'mobile')


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化
    """

    code = serializers.CharField(label='验证码', required=True, write_only=True, min_length=4, max_length=4,
                                 help_text='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'min_length': '验证码格式错误',
                                     'max_length': '验证码格式错误',
                                 })

    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')])
    password = serializers.CharField(style={'input_type': 'password'}, label='密码', write_only=True)

    def create(self, validated_data):
        user = super().create(validated_data=validated_data)
        # 密码加密保存
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_code(self, code):
        # 验证码在数据库中是否存在，用户从前端 post 过来的值都会放入 initial_data 里面，排序(最新一条)
        # username 就是用户注册的手机号，验证码按添加时间倒序排序，为了后面验证过期，错误等
        verify_records = AuthCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            # 最近的一个验证码
            last_record = verify_records[0]

            # 有效期为五分钟
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')

            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        """
        可以作用于所有字段
        不加字段名的验证器作用于所有字段之上
        :param attrs:
        :return:
        """
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')
