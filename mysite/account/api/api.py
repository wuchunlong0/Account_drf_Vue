# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from account.models import Company, Material, Order
from account.views import  _getOperators , _filterOrder
from myAPI.pageAPI import djangoPage,PAGE_NUM,toInt
from myAPI.modelAPI import get_model_values
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from myAPI.searchAPI import SearchNameContact


@login_required
def billingFun(request, page):
    operators = _getOperators()     
    cleanData = request.GET.dict()
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items() ])    
    orders, monthNum = _filterOrder(request, cleanData)      
    TotalTax = sum(orders.values_list('priceIncludeTax', flat=True))
    orders = orders.order_by('-date', '-id') 
    order_list =list(orders.values())
    order_list, pageList, num_pages, page = djangoPage(order_list ,page,PAGE_NUM)  #调用分页函数    
    order_list = list(get_model_values(order_list,[dict(author=User),dict(company=Company),dict(material=Material)])) #获得外键字段值   
    offset = PAGE_NUM * (page - 1)
    operators = [str(o) for o in operators] #数据库记录      
    username = request.user.username    
    mdict = {}
    if username in operators: #如果登录用户在Operator组
        company_name_list = Company.objects.values_list('name', flat=True)
        company_name_list = list(company_name_list) 
        type_list = [i[0] for i in Order.ORDER_TYPE]
        material_name_list = list(Material.objects.values_list('name', flat=True))
        taxPercent_list = [i[0] for i in Order.ORDER_TAX]      
        mdict = {'company_name_list':company_name_list,'type_list':type_list,\
                 'material_name_list':material_name_list,\
                 'taxPercent_list':taxPercent_list}     
    
    mydict = {'order_list':order_list,'pageList':pageList,\
              'num_pages': num_pages,'page': page,'offset':offset,\
              'operators':operators,'monthNum':monthNum,'cleanData':cleanData,\
              'queryString':queryString,'username':username}     
    mydict.update(mdict)
    return mydict

@login_required
def billing(request, page):
    mydict = billingFun(request, page)
    return JsonResponse(mydict,safe=False)

@login_required   
def customer(request, page): 
    operators = _getOperators()
    
    if request.user not in operators:
        return HttpResponseRedirect('/')         
    cleanData = request.GET.dict() 
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items() ])        
    companys = SearchNameContact(Company, cleanData.get('name',''),cleanData.get('contact',''))
    companys = companys.order_by('-id')
    companys =list(companys.values())
    company_list, pageList, num_pages, page = djangoPage(companys,page,PAGE_NUM)  #调用分页函数
    company_list = list(get_model_values(company_list,[dict(username=User)])) #获得外键字段值   
    offset = PAGE_NUM * (page - 1)
    operators = [str(o) for o in operators] #数据库记录   
    mydict = {'company_list':company_list,'pageList':pageList,\
              'num_pages': num_pages,'page': page,'offset':offset,\
              'operators':operators,'cleanData':cleanData,'queryString':queryString}     
    return JsonResponse(mydict,safe=False)    

@login_required 
def operator(request):
    operators = _getOperators()
    operators = [str(o) for o in operators] #数据库记录 
    username = request.user.username
    mydict = {'operators':operators,'username':username }
    return JsonResponse(mydict,safe=False)  

# http://localhost:8000/api/test/
def test(request, page):
    return HttpResponse('api ok')    
