from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    # 第三方应用：django 开发之性能强大的检测工具
    'debug_toolbar',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

## 数据库相关配置

DATABASES = {
    # 指定默认的数据库
    'default': {
        # 数据库引擎
        'ENGINE': 'django.db.backends.mysql',
        # 数据库名
        'NAME': config('DB_MYSQL_NAME'),
        'HOST': 'localhost',
        'USER': config('DB_MYSQL_USER', default=''),
        'PASSWORD': config('DB_MYSQL_PASSWORD', default=''),
        'PORT': config('DB_MYSQL_PORT', default=3306, cast=int),
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB; SET foreign_key_checks = 0;'}
    }
}

## DEBUG TOOLBAR 相关配置

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    # Toolbar options
    'RESULTS_CACHE_SIZE': 3,
    "JQUERY_URL": '//cdn.bootcss.com/jquery/2.2.4/jquery.min.js',
    'SHOW_COLLAPSED': True,
    # Panel options
    'SQL_WARNING_THRESHOLD': 100,   # milliseconds
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
}
