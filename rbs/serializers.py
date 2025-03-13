from rest_framework import serializers
from rbs.models import Category,Product,Table
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","password","email"]
        read_only_fields=["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model=Table
        fields="__all__"
        read_only_fields=["id"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"
        read_only_fields=["id"]

class ProductSerializer(serializers.ModelSerializer):
    category_object=serializers.StringRelatedField()
    class Meta:
        model=Product
        fields="__all__"
        read_only_fields=["id","category_object"]