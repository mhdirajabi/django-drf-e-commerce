from rest_framework import serializers
from shop.models import Cart, CartItem
from shop_management.models import Product, Shop, ShopType


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            "name",
            "type",
            "image",
        )
        depth = 1


class ShopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopType
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "brand",
            "description",
            "price",
            "image",
            "category",
        ]
        depth = 2


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CarItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "product",
        ]
        extra_kwargs = {
            "cart": {
                "allow_null": True,
            },
        }


class DeleteCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
