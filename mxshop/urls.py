"""mxshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from rest_framework_jwt.views import obtain_jwt_token

from mxshop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet

router = DefaultRouter()

# 配置 goods 的 URL
router.register('goods', GoodsListViewSet, base_name='goods')

# 配置 category 的 URL
router.register('categories', CategoryViewSet, base_name='categories')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    path('docs/', include_docs_urls(title='mxshop')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),

    # jwt 的认证接口
    path('login/', obtain_jwt_token),
]
