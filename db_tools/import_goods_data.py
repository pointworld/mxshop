#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

__author__ = 'point'
__date__ = '2018-12-22'

"""
独立使用 Django 的 model，导入商品数据
"""


import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')
# manage.py 中
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mxshop.settings')

import django
django.setup()


from goods.models import Goods, GoodsCategory, GoodsImage
from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail['name']
    goods.market_price = float(int(goods_detail['market_price'].replace('￥', '').replace('元', '')))
    goods.shop_price = float(int(goods_detail['sale_price'].replace('￥', '').replace('元', '')))
    goods.brief = goods_detail['desc'] if goods_detail['desc'] is not None else ''
    goods.desc = goods_detail['goods_desc'] if goods_detail['goods_desc'] is not None else ''
    # 取第一张作为封面图
    goods.cover = goods_detail['images'][0] if goods_detail['images'] else ''

    category_name = goods_detail['categorys'][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail['images']:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()
