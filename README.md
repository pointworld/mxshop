# 基于 DRF + Vue 的在线生鲜超市

## 亮点

- DRF + Vue 实现前后端分离

- 玩转 restful api 开发流程

- DRF 功能实现和核心源码分析

- 文档自动化管理

- 系统优化

  - DRF 的缓存

- 反爬措施

  - throttling 对用户和 IP 进行限速

- Sentry 完成线上系统错误日志的监控和告警

- 第三方登录

- 集成支付宝

- 微信推送消息

## 系统构成

- Vue 前端项目

- 基于 DRF 实现的主站

- 基于 simpleui 实现的后台管理系统，集成 froala 富文本编辑器

## 系统拆分

- 商品系统

- 用户系统

- 订单系统

- 购物车系统

- 支付系统

- 通知系统

- 后台管理系统

## 开发环境

操作系统: MacOS, Linux
开发工具: PyCharm + Vim
后台语言: Python@3.7.x
后台框架: Django@2.1.x
数据库: MariaDB、Redis
版本管理工具: Git

## 后端核心环境依赖

coreapi==2.3.3
Django==2.1.4
django-cors-headers==2.4.0x
django-filter==2.0.0
django-froala-editor==3.0.5
django-guardian==1.4.9
django-redis==4.10.0
django-simpleui==2.8
djangorestframework==3.10.2
djangorestframework-jwt==1.11.0
djangorestframework-simplejwt==3.3
drf-extensions==0.5.0
mysqlclient==1.3.13
Pillow==5.3.0
python-social-auth==0.3.6
redis==3.3.8
requests==2.21.0
social-auth-core==3.2.0

## DRF 项目结构


