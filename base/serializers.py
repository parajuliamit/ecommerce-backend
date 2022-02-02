from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

from .models import *

class RegisterUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 100)

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','email','name']

    def get_name(self,obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','email','name','token']
    
    def get_token(self,obj):
        token = AccessToken.for_user(obj)
        return str(token)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['product','quantity']

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','total','date_ordered','status']

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['shipping_address','phone_number','payment_method','payment_status']

class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)
          
    class Meta:
        model = Order
        fields = '__all__'

    def get_items(self,obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items,many=True)
        return serializer.data
