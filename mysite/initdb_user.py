# -*- coding: UTF-8 -*-
import os
import sys
import django
import random
import datetime

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    from django.contrib.auth.models import User, Group, Permission
    from account.models import Material, Order, Company
    
    operatorGroup = Group.objects.create(name='Operator')
    operatorGroup.permissions.add(Permission.objects.get(name='Can add company'),\
                        Permission.objects.get(name='Can add order'))#组添加权限 
    
    customerGroup = Group.objects.create(name='Customer')
    
    user = User.objects.create_superuser('admin', 'admin@test.com',
                                         '1234qazx')
    user.save()
    
    OPEERATOR_NUM = 4
    COMPANY_NUM = 35
    
    for i in range(OPEERATOR_NUM):
        user = User.objects.create_user('op%s' % i, 'op%s@test.com' % i,
                                        '1234qazx')
        user.is_staff = True
        user.is_superuser = False
        user.groups.add(operatorGroup)
        user.save()      
    
    
    for i in range(COMPANY_NUM):
        user = User.objects.create_user('cx%s' % i, 'cx%s@test.com' % i,
                                        '1234qazx')
        user.is_staff = True
        user.is_superuser = False
        user.groups.add(customerGroup)
        user.save()   
  