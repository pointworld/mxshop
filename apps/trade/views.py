from datetime import datetime

from django.shortcuts import redirect
from django.conf import settings

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerOrReadOnly
from utils.alipay import AliPay
from .serializers import CartSerializer, CartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import Cart, Order, OrderGoods


class CartViewSet(viewsets.ModelViewSet):
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
    serializer_class = CartSerializer

    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return CartDetailSerializer
        else:
            return CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    # 库存数-1
    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.stock_nums -= 1
        goods.save()

    # 库存数+1
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.stock_nums += 1
        goods.save()
        instance.delete()

    # 更新库存
    def perform_update(self, serializer):
        cart = Cart.objects.get(id=serializer.instance.id)
        nums_in_cart = cart.nums
        saved_record = serializer.save()
        # 变化的数量
        nums = nums_in_cart - saved_record.nums
        goods = saved_record.goods
        goods.stock_nums += nums
        goods.save()


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shopping_carts = Cart.objects.filter(user=self.request.user)
        for shopping_cart in shopping_carts:
            order_goods = OrderGoods()
            order_goods.goods = shopping_cart.goods
            order_goods.goods_nums = shopping_cart.nums
            order_goods.order = order
            order_goods.save()

            shopping_cart.delete()
        return order


class AlipayView(APIView):
    def get(self, request):
        """
        处理支付宝的 return_url 返回
        :param request:
        :return:
        """

        processed_dict = {}
        # 获取 GET 中参数
        for key, value in request.GET.items():
            processed_dict[key] = value

        # 取出 sign
        sign = processed_dict.pop('sign', None)

        # 测试用例
        alipay = AliPay(
            # appid 在沙箱环境中就可以找到
            appid="2016092300575055",
            # 这个值先不管，在与 vue 的联调中介绍
            app_notify_url="http://132.232.184.182:8000/alipay/return/",
            # 我们自己商户的密钥
            app_private_key_path=settings.PRIVATE_KEY_PATH,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_path=settings.ALIPAY_PUB_KEY_PATH,
            # 先不用管，后面 vue 解释
            return_url="http://132.232.184.182:8000/alipay/return/",
            # debug 为 true 时使用沙箱的 url。如果不是则用正式环境的 url，默认 False
            debug=True,
        )

        verify_ret = alipay.verify(processed_dict, sign)
        # 这里可以不做操作。因为不管发不发 return url。notify url 都会修改订单状态
        if verify_ret is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            # FIXME: 支付宝接口会先发起post请求，再响应get请求。而returnurl的返回参数中并不包含我们的支付状态，所以会导致原本被post请求写入的支付状态被get请求获取不到的默认值none覆盖为空
            # trade_status = processed_dict.get('trade_status', None)
            trade_status = processed_dict.get('trade_status', 'TRADE_SUCCESS')

            existed_orders = Order.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect('/index/#/app/home/member/order')
            # response.set_cookie('nextPath', 'pay', max_age=2)

            return response
        else:
            return redirect('index')

    def post(self, request):
        """
        处理支付宝的 notify_url
        :param request:
        :return:
        """

        # 1. 先将 sign 剔除掉
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop('sign', None)

        # 2. 生成一个 Alipay 对象
        alipay = AliPay(
            # appid 在沙箱环境中就可以找到
            appid="2016092300575055",
            # 这个值先不管，在与 vue 的联调中介绍
            app_notify_url="http://132.232.184.182:8000/alipay/return/",
            # 我们自己商户的密钥
            app_private_key_path=settings.PRIVATE_KEY_PATH,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_path=settings.ALIPAY_PUB_KEY_PATH,
            # 先不用管，后面 vue 解释
            return_url="http://132.232.184.182:8000/alipay/return/",
            # debug 为 true 时使用沙箱的 url。如果不是则用正式环境的 url，默认 False
            debug=True,
        )

        # 3. 进行验签，确保这是支付宝给我们的
        verify_ret = alipay.verify(processed_dict, sign)

        # 如果验签成功
        if verify_ret is True:
            # 商户网站唯一订单号
            order_sn = processed_dict.get('out_trade_no', None)
            # 支付宝系统交易流水号
            trade_no = processed_dict.get('trade_no', None)
            # 交易状态
            trade_status = processed_dict.get('trade_status', None)

            # 查询数据库中存在的订单
            existed_orders = Order.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:

                # 商品销量
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_nums += order_good.goods_nums
                    goods.save()

                # 更新订单状态
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            # #需要返回一个 'success' 给支付宝，如果不返回，支付宝会一直发送订单支付成功的消息
            return Response('success')
