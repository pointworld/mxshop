from random import choice

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import mixins, permissions, authentication
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import AuthCode
from .serializers import SmsSerializer, UserRegisterSerializer, UserDetailSerializer
from utils.yunpian import YunPian

User = get_user_model()


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """

    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """

        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # 有效性验证失败会直接抛异常（400 页面）
        serializer.is_valid(raise_exception=True)

        yun_pian = YunPian(settings.YUNPIAN_APIKEY)

        mobile = serializer.validated_data['mobile']
        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = AuthCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """

    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        """
        动态选择用哪个序列化方式
        :return:
        """
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer

    def get_permissions(self):
        """
        这里需要动态权限配置
        1. 用户注册的时候不应该有权限限制
        2. 当想获取用户详情信息的时候，必须登录才行
        :return:
        """
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        ret_dict = serializer.data
        payload = jwt_payload_handler(user)
        ret_dict['token'] = jwt_encode_handler(payload)
        ret_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """
        获取登录的用户
        :return:
        """
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
