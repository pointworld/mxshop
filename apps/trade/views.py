# Create your views here.

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer
from .models import ShoppingCart


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能开发
    list:
        获取购物车详情
    delete:
        删除购物记录
    create:
        加入购物车
    retrieve:
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShoppingCartSerializer

    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer


    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)