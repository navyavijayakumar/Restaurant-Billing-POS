from rest_framework import serializers
from rbs.models import Category,Product,Table,Order,OrderItems
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

class OrderSerializer(serializers.ModelSerializer):
    all_items=serializers.SerializerMethodField(read_only=True)
    table_object=serializers.StringRelatedField()
    item_count=serializers.SerializerMethodField(read_only=True)
    bill_total=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=Order
        fields="__all__"
        read_only_fields=["id","table_object"]

    def get_all_items(self,obj):
        qs=obj.items.all()
        serializer_instance=OrderItemSerializer(qs,many=True)
        return serializer_instance.data

    def get_item_count(self,obj):
        return OrderItems.objects.filter(order_object=obj).count()
    
    def get_bill_total(self,obj):
        order_items=OrderItems.objects.filter(order_object=obj)
        total=sum([oi.product_object.price * oi.qty for oi in order_items])
        return total
        
class OrderItemSerializer(serializers.ModelSerializer):
    product_object=serializers.StringRelatedField()
    item_total=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=OrderItems
        fields="__all__"
        read_only_fields=["id","order_object"]

    def get_item_total(self,obj):
        price=obj.product_object.price
        total=obj.qty * price
        return total