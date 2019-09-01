from .base import *

DEBUG = False

## 缓存相关配置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

## 一个字符串列表，用来表示 Django 站点可以服务的 host/domain
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

## 数据库相关配置

# MYSQL 相关配置
DATABASES = {
    # 指定默认的数据库
    'default': {
        # 数据库引擎
        'ENGINE': 'django.db.backends.mysql',
        # 数据库名
        'NAME': config('DB_MYSQL_NAME'),
        'HOST': config('DB_MYSQL_HOST', default='localhost'),
        'USER': config('DB_MYSQL_USER', default=''),
        'PASSWORD': config('DB_MYSQL_PASSWORD', default=''),
        'PORT': config('DB_MYSQL_PORT', default=3306, cast=int),
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB; SET foreign_key_checks = 0;'}
    }
}

# REDIS 相关配置
REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = 0
REDIS_PASSWORD = config('REDIS_PASSWORD', default='')

## 邮箱相关配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
