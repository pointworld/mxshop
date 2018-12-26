#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
from django.db.models import Q

__author__ = 'point'
__date__ = '2018-12-22'

from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexGoodsAd


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ('name', 'hit_nums', 'market_price', 'add_time',)
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexGoodsAd.objects.filter(category_id=obj.id)
        if ad_goods:
            inner_goods = ad_goods[0].goods
            goods_json = GoodsSerializer(inner_goods, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(
            Q(category_id=obj.id)
            | Q(category__parent_category_id=obj.id)
            | Q(category__parent_category__parent_category_id=obj.id)
        )
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'
