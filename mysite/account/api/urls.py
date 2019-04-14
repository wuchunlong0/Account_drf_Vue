# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import api
# http://localhost:8000/api/billing/
# http://localhost:8000/api/customer/
# http://localhost:8000/api/operator/
urlpatterns = [
    url(r'^billing/(?P<page>\d*)?$', api.billing, name='billing_api'),
    url(r'^customer/(?P<page>\d*)?$', api.customer, name='customer_api'),    
    url(r'^operator/$', api.operator, name='operator_api'), 
    url(r'^test/(?P<page>\d*)?$', api.test, name="test"),

]
