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
        # 不管当前点击的是一级分类二级分类还是三级分类，都能找到
        return queryset.filter(
            Q(category_id=value)
            | Q(category__pid_id=value)
            | Q(category__pid__pid_id=value)
        )

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'is_hot', 'is_new']
