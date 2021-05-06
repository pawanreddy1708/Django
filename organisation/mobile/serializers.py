from rest_framework import serializers
from .models import Products,WishList

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['brand','model','description','price','quantity']

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ['owner','products']