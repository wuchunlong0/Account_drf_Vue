# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^billing_vue/(?P<page>\d*)?$', views.billing_vue, name='billing_vue'),
    url(r'^customer_vue/(?P<page>\d*)?$', views.customer_vue, name='customer_vue'),
    url(r'^add/billing_vue/$', views.addBilling_vue, name='add_billing_vue'),
    url(r'^add/customer_vue/$', views.addCustomer_vue, name='add_customer_vue'),
    url(r'^makexlsx/$', views.makexlsx, name="makexlsx"),
]
