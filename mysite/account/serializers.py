# -*- coding: utf-8 -*-
"""
from rest_framework import serializers 
from api.models import Product 
class ProductSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Product 
        fields = ('id', 'created', 'name', 'describe', 'price', 'isDelete')
"""
from .models import Company,Material,Order
from rest_framework import serializers

from django.contrib.auth.models import User, Group

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','url','email')


class CompanySerializer(serializers.ModelSerializer):
    username_name = serializers.CharField(source='username.username',read_only=True) #获得外键值
    class Meta:
        model = Company
        fields = ('id', 'name', 'taxNumber', 'address','bank', 'bankAccount',\
                   'contact', 'telephone','username','username_name')
 
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'price')
 
class OrderSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username',read_only=True) #获得外键值
    material_name = serializers.CharField(source='material.name',read_only=True) #获得外键值
    company_name = serializers.CharField(source='company.name',read_only=True) #获得外键值
    class Meta:
        model = Order
        fields = ('id', 'company', 'date', 'type','content', 'material',\
                  'sizeWidth', 'sizeHeight', 'priceMaterial', 'price',\
                  'quantity','priceTotal', 'taxPercent',\
                  'priceIncludeTax','checkout','author','author_name','material_name','company_name')

