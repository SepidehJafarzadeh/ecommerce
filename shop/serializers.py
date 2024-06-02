from rest_framework import serializers
from .models import Product, Category, Comment, Image, Feature, ProductFeature, Order
from shop.models import User


class OrderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class CategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductFeatureSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = "__all__"


class FeatureSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"

class CommentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class ImageSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
