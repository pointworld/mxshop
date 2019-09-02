import os
import sys
import datetime

from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['*']

# 此处重载是为了使我们的 UserProfile 生效
AUTH_USER_MODEL = 'users.UserProfile'

INSTALLED_APPS = [
    # 第三方应用：替换 Django 原生 admin 后台页面
    'simpleui',

    # 自定义应用：用户
    'users',
    # 自定义应用：商品
    'goods',
    # 自定义应用：交易
    'trade',
    # 自定义应用：用户操作
    'user_operation',

    # 第三方应用：前后端分离
    'rest_framework',
    # 第三方应用：过滤
    'django_filters',
    # 第三方应用：解决跨域问题
    'corsheaders',
    'rest_framework.authtoken',
    # 第三方应用：集成第三方登录
    'social_django',
    'froala_editor',

    # 原生应用
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # 第三方中间件：跨域中间件应该尽可能的放在前面
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 跨域配置
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'mxshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            # 上下文管理器
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # 第三方登录
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'mxshop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxshop',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {'init_command': 'SET default_storage_engine=INNODB;'},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 语言默认是 en-us，这里改为中文
LANGUAGE_CODE = 'zh-hans'

# 时区默认是 UTC，这里改为上海
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 数据库存储使用时间，设置为 True 的话，时间会被存为 UTC 的时间
USE_TZ = False

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# 设置上传文件的路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 认证
AUTHENTICATION_BACKENDS = (
    # 设置邮箱和用户名和手机号均可登录
    'users.utils.CustomBackend',
    # 第三方登录
    'social_core.backends.weibo.WeiboOAuth2',
    # 'social_core.backends.weixin.WeixinOAuth2',
    # 'social_core.backends.qq.QQOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    # 限流相关配置
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },

    # 用于修复打开 docs/ 时的 bug
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
}

JWT_AUTH = {
    # 'JWT_ENCODE_HANDLER':
    #     'rest_framework_jwt.utils.jwt_encode_handler',
    #
    # 'JWT_DECODE_HANDLER':
    #     'rest_framework_jwt.utils.jwt_decode_handler',
    #
    # 'JWT_PAYLOAD_HANDLER':
    #     'rest_framework_jwt.utils.jwt_payload_handler',
    #
    # 'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    #     'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    #
    # 'JWT_RESPONSE_PAYLOAD_HANDLER':
    #     'rest_framework_jwt.utils.jwt_response_payload_handler',

    # 'JWT_SECRET_KEY': settings.SECRET_KEY,
    # 'JWT_GET_USER_SECRET_KEY': None,
    # 'JWT_PUBLIC_KEY': None,
    # 'JWT_PRIVATE_KEY': None,
    # 'JWT_ALGORITHM': 'HS256',
    # 'JWT_VERIFY': True,
    # 'JWT_VERIFY_EXPIRATION': True,
    # 'JWT_LEEWAY': 0,
    # 设置 token 过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),
    # 'JWT_AUDIENCE': None,
    # 'JWT_ISSUER': None,
    #
    # 'JWT_ALLOW_REFRESH': False,
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    # JWT 跟前端保持一致，比如 “token” 这里设置成 JWT
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    # 'JWT_AUTH_COOKIE': None,
}

# 手机号码的正则表达式
REGEXP_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'

## 云片网设置
YUNPIAN_APIKEY = config('YUNPIAN_APIKEY')
YUNPIAN_TEST_MOBILE = config('YUNPIAN_TEST_MOBILE')
YUNPIAN_SIGNATURE = config('YUNPIAN_SIGNATURE')

## 支付宝相关配置
ALIPAY_APP_ID = config('ALIPAY_APP_ID')
ALIPAY_PRI_KEY_PATH = os.path.join(BASE_DIR, config('ALIPAY_PRI_KEY_PATH'))
ALIPAY_PUB_KEY_PATH = os.path.join(BASE_DIR, config('ALIPAY_PUB_KEY_PATH'))
ALIPAY_APP_NOTIFY_URL=config('TEST_SERVER') + '/alipay/return/'

## DRF 插件相关设置
REST_FRAMEWORK_EXTENSIONS = {
    # 这个缓存使用的是内存，每次重启之后就会失效
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60 # 1h 过期
}

## 配置 Redis 缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

## 第三方登录

SOCIAL_AUTH_WEIBO_KEY = config('SOCIAL_AUTH_WEIBO_KEY')
SOCIAL_AUTH_WEIBO_SECRET = config('SOCIAL_AUTH_WEIBO_SECRET')

SOCIAL_AUTH_QQ_KEY = config('SOCIAL_AUTH_QQ_KEY')
SOCIAL_AUTH_QQ_SECRET = config('SOCIAL_AUTH_QQ_SECRET')

SOCIAL_AUTH_WEIXIN_KEY = config('SOCIAL_AUTH_WEIXIN_KEY')
SOCIAL_AUTH_WEIXIN_SECRET = config('SOCIAL_AUTH_WEIXIN_SECRET')

# 用户登录成功之后，页面跳转
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'
