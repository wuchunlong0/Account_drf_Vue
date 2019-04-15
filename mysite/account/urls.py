# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from rest_framework import routers
router = routers.DefaultRouter()

# http://127.0.0.1:8000/account/materials/1
# http://127.0.0.1:8000/account/companys/
#这里，不支持的带页的路由 router.register(r'orders/(?P<page>\d*)?$', views.OrderViewSet)
router.register(r'companys', views.CompanyViewSet)
router.register(r'materials', views.MaterialViewSet)

from django.urls import path, include
urlpatterns = [    
    url(r'^makexlsx/$', views.makexlsx, name="makexlsx"),
    url(r'^billing_vue/$', views.billing_vue, name='billing_vue'),
    url(r'^customer_vue/$', views.customer_vue, name="customer_vue"),

    url(r'^add/billing_vue/$', views.addBilling_vue, name='add_billing_vue'),        
    url(r'^addcustomer_vue/$', views.addCustomer_vue, name='add_customer_vue'),    
    url(r'^api/$', views.api, name="api"),    
    url(r'^test/$', views.test, name="test"),  
    
    url(r'^', include(router.urls)), 
     
    url("^orderlist/$", views.Orderlist.as_view()),    
    url("^customerlist/$", views.customerlist.as_view()),
            
    url('api-auth/', include('rest_framework.urls')), #右上角注册登录控件
]
