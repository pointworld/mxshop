# 项目开发文档

## 目标

开发一个前后端分离的在线生鲜超市

## 需求

### 功能组成

- 用户系统

  - 登录和注册
  
  - 个人中心
  
    - 我的个人信息
  
    - 我的消息
    
    - 我的订单
    
    - 访问历史
    
- 商品系统
  
  - 商品分类
    
  - 热卖商品
    
  - 最新商品
    
- 订单系统
  
- 购物车系统

- 支付系统

  - 微信支付
  
  - 支付宝支付

- 通知系统

  - 站内通知
  
  - 站外通知
  
    - 短信通知
    
    - 微信通知
    
    - 邮箱通知
    
- 后台管理系统

  - 用户系统
  
    - 增删查改
    
  - 商品系统
  
    - 增删查改
    
  - 权限系统
  
  - CMDB
  
  - RBAC
  
  - 消息系统
  
  - 日志管理系统
  
## 前端

### 架构

#### 页面组成

##### 首页

##### 商品列表

##### 商品搜索

##### 商品详情

##### 登录注册

##### 用户个人中心

##### 购物车

##### 订单

##### 支付

## 后端

### 架构

#### 表结构设计

##### 通用表字段

- 主键 id, int(11), not null, auto_increment
- 添加时间 add_time, datetime
- 更新时间 update_time, datetime(6), not null
- 删除时间 delete_time, datetime(6), not null

##### 用户相关（User）

- 用户表（UserProfile）
  
  - *用户存放用户个人信息*
  
  - 继承 AbstractUser
  
  - 姓名 name: varchar(32), unique, default null
  - 出生日期 birthday: date, default null
  - 性别 gender: varchar(6), not null
  - 手机号 mobile: char(11), default null
  - 邮箱 email: varchar(50), default null
  
- 验证码表（AuthCode）

  - *用于存放验证码相关信息*

  - 验证码 code: char(6), not null
  - 手机号 mobile: char(11), not null

##### 商品相关（Goods）

- 商品（Goods）

  - *用户存放商品相关信息*
  
  - 名称 name: varchar(100), not null
  - 序列号 sn: varchar(50), not null
  - 市场价 market_price: double, not null
  - 销售价 shop_price: double, not null
  - 封面 cover: varchar(100), default null
  - 简介 brief: longtext, not null
  - 描述 desc: longtext, not null
  - 所属分类 category: foreign key, int(11), not null
  - 点击数 hit_nums: int(11), not null
  - 收藏数 fav_nums: int(11), not null
  - 库存数 stock_nums: int(11), not null
  - 销售量 sold_nums: int(11), not null
  - 是否免运费 freight_free: tinyint(1), not null
  - 是否新品 is_new: tinyint(1), not null
  - 是否热销 is_hot: tinyint(1), not null

- 商品类别表（Category）

  - 名称 name: varchar(32), not null
  - 类目code code: varchar(32), not null
  - 描述 desc: longtext, not null
  - 级别 level: int(11), not null
  - 父类别 pid: foreign key, default null
  - 是否导航 is_tab: tinyint(1), not null, 针对一级类目

- 首页商品轮播表（IndexSlide）
  
  - *首页的商品轮播图片是大图，跟商品详情里面的图片不一样，所以要单独写一个首页轮播图 model*
  
  - 商品 goods: foreign key, int(11), not null
  - 轮播图 image: varchar(100), not null
  - 轮播顺序 index: int(11), not null

- 商品详情页轮播表（DetailSlide）

  - *首页的商品轮播图片是大图，这里是小图*

  - 商品 goods: foreign key, int(11), not null
  - 轮播图 image: varchar(100), not null
  - 轮播顺序 index: int(11), not null

- 商品热搜词表（HotSearchWords）

  - *搜索栏下面的热搜词*
  
  - 热搜词 keywords: varchar(20), not null
  - 排序 index: int(11), not null
  

##### 交易相关（Trade）

- 购物车（Cart）

  - 用户 user: primary key, int(11), not null
  - 商品 goods: primary key, int(11), not null
  - 购买数量 nums: int(11), not null
  
  - *unique(user, goods)*

- 订单（Order）

  - 订单序列号 order_sn: varchar(30), default null
  - 用户 user: foreign key, int(11), not null
  - 随机加密串 nonce_str: varchar(50), default null
  
  - 支付宝交易号 trade_no: varchar(100), default null
  - 支付状态 pay_status: varchar(20), not null
  - 支付类型 pay_type: varchar(20), not null
  - 支付时间 pay_time: datetime(6), default null
  
  - 订单留言 leave_msg: varchar(200), not null
  - 订单金额 order_amount: double, not null
  
  - 收货人地址 address: varchar(20), not null
  - 签收人名称 signer_name: varchar(20), not null
  - 签收人电话 signer_mobile: varchar(11), not null
  
  - *unique: order_sn, trade_no, nonce_str*
 
- 订单内商品（OrderGoods） 
  
  - *订单内的商品详情*
  
  - 订单 order: foreign key, int(11), not null
  - 商品 goods: foreign key, int(11), not null
  - 商品数量 goods_nums: int(11), default 0
  

##### 用户操作相关（user_operation）

- 用户收藏（user_fav）
  
  - 用户 user: foreign key, int(11), not null
  - 商品 goods: foreign key, int(11), not null
  
  - *unique(user, goods)*

- 用户收货地址（UserAddress）

  - 用户 user: foreign key, int(11), not null
  - 省份 province: varchar(100), not null
  - 城市 city: varchar(100), not null
  - 区域 distinct: varchar(100), not null
  - 详细地址 address: varchar(100), not null
  - 签收人名称 signer_name: varchar(30), not null
  - 签收人手机号 signer_mobile: varchar(11), not null
  
- 用户留言（UserLeavingMsg）

  - 用户 user: foreign key, int(11), not null
  - 类型 type: int(11), not null
  - 主题 subject: varchar(100), not null
  - 内容 content: longtext, not null
  - 文件 file: varchar(100), not null
  

### 项目目录结构搭建

- 项目根目录下新建两个 python package

  - extra_apps   （扩展的源码包）
  - apps         （放所有 app）

- 项目根目录下新建两个文件夹
  
  - media       （保存图片）
  - db_tools    （数据库相关）

### 项目配置

## 开发

### 用户登录与注册

#### 用户认证

##### DRF 原生提供的 token 认证

- DRF token('rest_framework.authtoken') 的缺点

  - 保存在数据库中，如果是一个分布式的系统，就非常麻烦
  - token 永久有效，没有过期时间

##### 第三方包 jwt 实现 token 认证

- 参见：http://getblimp.github.io/django-rest-framework-jwt/

- 安装
```bash
pip install djangorestframework-jwt
```

- 使用
```python
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}
```

```python
# urls.py

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

# jwt的 token 认证接口
path('jwt-auth/', obtain_jwt_token)
```

- 存在的问题

  - jwt 默认采用的是用户名和密码登录验证，如果用手机登录的话，就会验证失败，所以我们需要自定义一个用户验证

- 自定义用户认证

```python
# settings.py

AUTHENTICATION_BACKENDS = (
    # 自定义用户验证规则
    'users.views.CustomBackend',
)
```

##### 云片网发送短信验证码

###### 注册云片网

- “开发认证” -->> “签名管理” -->> “模板管理”

- 还要添加 IP 白名单，测试就用本地 IP，部署的时候一定要换成服务器的 IP

###### 发送验证码（简单实现）

apps 下新建 utils 文件夹。再新建 yunpian.py，代码如下：

```python
# apps/utils/yunpian.py

import json

import requests

class YunPian:

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"
    
    def send_msm(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【慕学生鲜】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)'
        }
        
        res = requests.post(self.single_send_url, data=params)
        
        return json.loads(res.text)


if __name__ == '__main__':
    yun_pian = YunPian('api_key_xxx')
    yun_pian.send_msm('2019', '手机号码')
    
```

####### DRF 实现发送短信验证码

- 手机号验证：

  - 是否合法
  - 是否已经注册
  
- settings.py
```python
# 手机号码正则表达式
REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'

```

- users 下新建 serializers.py，代码如下：
```python
# users/serializers.py

import re
from datetime import datetime, timedelta

from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import AuthCode


User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    
    # 函数名必须：validate_ + 验证字段名
    def validate_mobile(self, mobile):
        """
        手机号验证
        """
        
        # 是否已经注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('该手机号已被注册')
            
        # 是否合法
        if not re.match(settings.REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号格式不正确')
            
        # 验证码发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if AuthCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送未超过 60s')
        
        return mobile

```

- 将 APIKEY 放到 settings 中
```python
# 云片网 APIKEY
APIKEY = "xxxxx327d4be01608xxxxxxxxxx"
```

- views 后台逻辑
```python
from random import choice

from django.conf import settings

from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from users.serializers import SmsSerializer
from utils.yunpian import YunPian
from users.models import AuthCode


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    手机验证码
    """
    
    serializer_class = SmsSerializer
    
    def generate_code(self):
        """
        生成四位数字的验证码
        """
        
        seeds = '1234567890'
        random_str = []
        
        for i in range(4):
            random_str.append(choice(seeds))
            
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 验证合法性
        serializer.is_valid(raise_exception=True)
        
        mobile = serializer.validated_data['mobile'] 
        # 生成验证码
        code = self.generate_code()
        
        yun_pian = YunPian(settings.APIKEY)
        
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        
        # code 为 0 表示发送成功
        if sms_status['code'] != 0:
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
            
        code_record = AuthCode(code=code, mobile=mobile)
        code_record.save()
        
        return Response({
        'mobile': mobile
        }, status=status.HTTP_201_CREATED)

```

- 配置 URL
```python
from rest_framework.routers import DefaultRouter

from users.views import SmsCodeViewSet

router = DefaultRouter()

router.register(r'code', SmsCodeViewSet, base_name='code')

```

#### 用户注册

- 用户用手机号注册，需要填写手机号、验证码、密码

##### users/serializers.py

```python
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import AuthCode

User = get_user_model()


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
```

##### users/views.py

```python
from django.contrib.auth import get_user_model

from rest_framework import mixins, permissions, authentication
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.serializers import UserRegisterSerializer, UserDetailSerializer

User = get_user_model()


class UserViewSet(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """

    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer

    def get_permissions(self):
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
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
```

##### urls.py

```python
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router = DefaultRouter()

# 配置 Users 的 URL
router.register('users', UserViewSet, base_name='users')
```

##### Django 信号量实现用户密码修改

- users/signals.py
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()


# post_save: 接收信号的方式
# sender: 接收信号的 model
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为 update 的时候也会进行 post_save
    if created:
        password = instance.password
        #instance 相当于 user
        instance.set_password(password)
        instance.save()
```

- users/app.py
```python
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户管理"

    def ready(self):
        import users.signals
```

AppConfig 自定义的函数，会在 Django 启动时被运行

现在添加用户的时候，密码就会自动加密存储

##### 生成 token

- 生成 token 的两个重要步骤，一是 payload，二是 encode

```python
from django.contrib.auth import get_user_model

from rest_framework import mixins, permissions, authentication
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.serializers import UserRegisterSerializer, UserDetailSerializer

User = get_user_model()


class UserViewSet(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """

    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer

    def get_permissions(self):
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
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
```

##### 测试和联调

#### 用户登录

##### social_django 集成第三方登录

###### 微博登录

1. 申请应用

  - 进入微博开放平台，首先要经过认证，然后才可以创建应用

  - 地址：http://open.weibo.com/authentication

###### 微信登录

###### QQ 登录

### 商品

#### 商品列表

#### 商品详情

### 用户操作

### 用户个人中心

#### 用户收藏

#### 用户留言

#### 用户地址

### 交易

#### 购物车

##### 添加商品到购物车

#### 订单管理

#### 支付

##### 支付宝沙箱环境配置

###### 创建应用

- 进入蚂蚁金服开放平台（https://open.alipay.com/platform/home.htm），登录后进入开发中心 -->> 网页&移动应用
  
- 进入创建应用 - 支付接入，然后创建应用

- 创建应用后会有一个 appid。还需要提交信息进行审核。微信支付和支付宝支付都是要求企业认证才可以完成的，个人开发不可以，所以我们需要用沙箱环境，它可以让我们不具备这些应用或者说应用审核还没通过的时候先开发调试

###### 沙箱环境

- 沙箱应用地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info

- 公钥和私钥的生成方法
  - https://docs.open.alipay.com/291/105971/

- 把生成的公钥和私钥拷贝到trade/keys下面--->>>重命名--->>首位各添加下面的内容
  
  -----BEGIN PRIVATE KEY-----
  -----END PRIVATE KEY-----

- 把支付宝公钥也拷贝到这路径下面，同样首尾添加如上内容

- 文档说明

  - https://docs.open.alipay.com/270/105900/
  - sign 签名
    - 筛选并排序
    - 拼接
    - 调用签名函数
    - 把生成的签名赋值给 sign 参数，拼接到请求参数中

##### 编写代码

`pip install pycryptodome`

###### utils 中新建 alipay.py

###### django 集成支付宝 notify_url 和 return_url

- 配置 url
```python
from django.urls import path

from trade.views import AlipayView

# 配置支付宝支付相关接口的url
path('alipay/return/', AlipayView.as_view())
```

- utils/alipay.py
```python
# 把 return_url 和 notify_url 都改成远程服务器的地址

return_url="http://xxx:8000/alipay/return/"

app_notify_url="http://xxx:8000/alipay/return/"
```

- settings.py
```python
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 支付宝相关的key
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048.txt')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_key_2048.txt')
```

- trade/views.py

- trade/serializers.py

- 测试代码

  - 需要在服务器上调试代码

### 首页、商品数量

#### 轮播图接口实现

#### 新品接口功能开发

#### 首页商品分类显示功能

#### 商品点击数和收藏数

##### 点击数

##### 收藏数

##### 用信号量实现

delete 和 create 的时候 django model 都会发送一个信号量出来，用信号量的方式代码分离性更好

- user_operation/signal.py
```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def create_user_fav(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为 update 时也会进行 post_save
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_user_fav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()

```

- user_operation/app.py
```python
from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'user_operation'
    verbose_name = '操作管理'

    def ready(self):
        import user_operation.signals
  
```

##### 商品库存和销量修改

- 商品库存数量的行为：

  - 新增商品到购物车
  - 修改购物车数量
  - 删除购物车记录

### 缓存和限速

- 为了加速网站的访问速度，将一些数据放到缓存当中，取数据的时候首先去缓存中去，然后再去数据库中取

#### DRF 的缓存设置

- 我们用 DRF 的一个扩展来实现缓存，github 上面的使用说明：http://chibisov.github.io/drf-extensions/docs/#caching

##### drf-extensions

###### 安装
```bash

pip install drf-extensions
```

###### 使用方法

- 导入和引用
```python
from rest_framework import mixins, viewsets
# 导入
from rest_framework_extensions.cache.mixins import CacheResponseMixin

# 在 GoodsListViewSet 中添加缓存功能

# CacheResponseMixin 一定要放在第一个位置

class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass

```

- 设置过期时间，settings 里面
```python
#缓存配置
REST_FRAMEWORK_EXTENSIONS = {
    # 这个缓存使用的是内存，每次重启之后就会失效
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 5   #5s 过期，时间自己可以随便设定
}
```

##### DRF 配置 redis 缓存

- 使用 django-redis 第三方库：http://django-redis-chs.readthedocs.io/zh_CN/latest/#id8（文档说明）

###### 安装

```bash
pip install django-redis
```

###### 作为 cache backend 使用配置

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

为了更好的互操作性并使连接字符串更加 “标准”, 从 3.8.0 开始 django-redis 使用 redis-py native url notation 作为连接字符串.

URL 格式举例
```text
redis://[:password]@localhost:6379/0          # 普通的 TCP 套接字连接
rediss://[:password]@localhost:6379/0         # SSL 包裹的 TCP 套接字连接
unix://[:password]@/path/to/socket.sock?db=0  # Unix 域套接字连接
```

指定数据库数字的方法:

  - db 查询参数, 例如: redis://localhost?db=0
  - 如果使用 redis:// scheme, 可以直接将数字写在路径中, 例如: redis://localhost/0

###### 作为 session backend 使用配置

Django 默认可以使用任何 cache backend 作为 session backend, 将 django-redis 作为 session 储存后端不用安装任何额外的 backend

```python

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

#### DRF 的 throttle 设置 api 的访问速率

- 为了防止爬虫对服务器造成的重大压力，对数据进行访问速率限制就显得非常的重要了

##### settings 中配置
```python
REST_FRAMEWORK = {
    # 限速设置
    'DEFAULT_THROTTLE_CLASSES': (
            'rest_framework.throttling.AnonRateThrottle',   # 未登陆用户
            'rest_framework.throttling.UserRateThrottle'    # 登陆用户
        ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/minute',         # 每分钟可以请求两次
        'user': '5/minute'          # 每分钟可以请求五次
    }
}
```

##### goods/views.py 中使用

```python

from rest_framework import mixins, viewsets
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from rest_framework_extensions.mixins import CacheResponseMixin


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass
    throttle_classes = (UserRateThrottle, AnonRateThrottle)

```


### vue 静态文件放到 django 中


### DRF 的 API 文档



## 测试

## 部署

### Django + nginx + uwsgi 部署

#### 原理

- Django
  - 一个基于 Python 的开源 web 框架
  
- uwsgi
  - 一个 web 服务器，也可以当作中间件
  
- nginx
  - 常用的高性能代理服务器
  
- wsgi.py 
  - Django 项目携带的一个 wsgi 接口文件

## 上线

 
 
