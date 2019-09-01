from django.db.models import Q

from rest_framework import serializers

from goods.models import Goods, Category, DetailSlide, IndexSlide, CategoryBrand, IndexGoodsAd


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class DetailSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSlide
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = DetailSlideSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ('name', 'hit_nums', 'market_price', 'add_time',)
        fields = '__all__'


class IndexSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexSlide
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryBrand
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
            | Q(category__pid_id=obj.id)
            | Q(category__pid__pid_id=obj.id)
        )
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = Category
        fields = '__all__'
