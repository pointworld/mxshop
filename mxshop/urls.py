from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from rest_framework_jwt.views import obtain_jwt_token

from mxshop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, IndexSlideViewSet, IndexCategoryViewSet
from trade.views import CartViewSet, OrderViewSet
from trade.views import AlipayView
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet

router = DefaultRouter()

# 配置 goods 的 URL
router.register('goods', GoodsListViewSet, base_name='goods')

# 配置 category 的 URL
router.register('categories', CategoryViewSet, base_name='categories')

# 配置短信验证码的 URL
router.register('codes', SmsCodeViewSet, base_name='codes')

# 配置 Users 的 URL
router.register('users', UserViewSet, base_name='users')

# 配置 用户收藏 的 URL
router.register('user_favs', UserFavViewSet, base_name='user_favs')

# 配置 用户留言 的 URL
router.register('user_message', UserLeavingMessageViewSet, base_name='user_message')

# 配置 用户地址 的 URL
router.register('user_address', UserAddressViewSet, base_name='user_address')

# 配置 购物车 的 URL
router.register('shopping_carts', CartViewSet, base_name='shopping_carts')

# 配置 订单 的 URL
router.register('orders', OrderViewSet, base_name='orders')

# 配置 首页轮播图 的 URL
router.register('banners', IndexSlideViewSet, base_name='banners')

# 配置 首页商品系列 的 URL
router.register('index_goods', IndexCategoryViewSet, base_name='index_goods')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # 接口文档
    path('docs/', include_docs_urls(title='mxshop')),
    path('api-auth/', include('rest_framework.urls')),
    path('froala_editor/', include('froala_editor.urls')),
    # 首页
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    # jwt 的认证接口
    path('login/', obtain_jwt_token),
    # 配置 支付宝 的接口
    path('alipay/return/', AlipayView.as_view(), name='alipay'),
    # 第三方登录
    path('', include('social_django.urls', namespace='social')),
]
