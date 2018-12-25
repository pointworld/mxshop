#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

__author__ = 'point'
__date__ = '2018-12-22'

from django.db.models import Q

import django_filters

from .models import Goods


class GoodsFilter(django_filters.filterset.FilterSet):
    """
    商品的过滤类
    """

    price_min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(
            Q(category_id=value)
            | Q(category__parent_category_id=value)
            | Q(category__parent_category__parent_category_id=value)
        )

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'is_hot']