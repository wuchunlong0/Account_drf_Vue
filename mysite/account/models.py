# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    taxNumber = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200)
    bank = models.CharField(max_length=200, null=True, blank=True)
    bankAccount = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    username = models.ForeignKey(User, on_delete=models.PROTECT, null=True,
                               blank=True) #客户名称
    def __str__(self): 
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField()    
    def __str__(self):
        return self.name

class Order(models.Model):
    ORDER_TYPE = (
        ('Design', 'Design'),
        ('Other', 'Other'),
        ('Manufacture', 'Manufacture'),
    )
    ORDER_TAX = (
        (0, 0),
        (6, 6),
        (17, 17),
    )
    
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True,
                               blank=True) #记录人
    #date = models.DateField(default=datetime.datetime.now) #日期
    date = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)#日期时间    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True,
                               blank=True) #公司
    type = models.CharField(max_length=20, choices=ORDER_TYPE,
                            default=ORDER_TYPE[0][0])  #类型
    content = models.CharField(max_length=200, default='') #内容
    material = models.ForeignKey(Material, on_delete=models.CASCADE,
                                 null=True, blank=True) #材料
    sizeWidth = models.FloatField(default=1, null=True, blank=True)
    sizeHeight = models.FloatField(default=1, null=True, blank=True)
    priceMaterial = models.FloatField(default=0, null=True, blank=True)
    price = models.FloatField(default=0) #单价 默认值0
    quantity = models.FloatField(default=1) #数量
    priceTotal = models.FloatField(default=0)
    taxPercent = models.FloatField(choices=ORDER_TAX, default=ORDER_TAX[0][0])
    priceIncludeTax = models.FloatField(default=0) #含税价
    checkout = models.BooleanField(default=False) #结算
    
    def _autoFill(self): #此函数在initdb.py、views.py（addBilling）中使用
        if self.type == 'Manufacture':
            self.priceMaterial = round(self.material.price, 2)
            self.price = round(self.sizeHeight * self.sizeWidth * self.priceMaterial, 2)
        self.priceTotal = round(self.price * self.quantity, 2)
        self.priceIncludeTax = round(self.priceTotal * 100 / (100 - self.taxPercent), 2)
    
    def __str__(self):
        content = self.content
        if len(content) > 10:
            content = content[:10]
        
        return '%s-(%s)' % (self.company, content)