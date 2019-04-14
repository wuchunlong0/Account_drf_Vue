# -*- coding: utf-8 -*-
import os,re,tempfile,datetime,uuid,xlsxwriter
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from monthdelta import monthdelta
from .models import Company, Material, Order
from django.contrib.auth.models import User, Group
from account.myAPI.download import downLoadFile
from account.myAPI.pageAPI import MyFormatResultsSetPagination,PAGE_NUM
from account.myAPI.fileAPI import ListToXlsx
from account.myAPI.searchAPI import SearchNameContact
from account.myAPI.modelAPI import get_model_values
from account.myAPI.listdictAPI import deldictNULL
from django.http import JsonResponse
from django.utils.decorators import method_decorator

# http://localhost:8000/account/test/?p=-1
def test(request):
    return JsonResponse({'a':-1})
    return HttpResponse('ok')

def _getOperators():
    operators = Group.objects.get(name='Operator').user_set.all()
    return [user for user in User.objects.all() if user.is_superuser or user in operators]

def _filterOrder(request, cleanData):
    orders = Order.objects
    operators = _getOperators()
    
    if request.user not in operators:
        orders = orders.filter(company__username=request.user)
    elif cleanData.get('company', ''):
        orders = orders.filter(company__name__icontains=cleanData['company'])
        
    if cleanData.get('content', ''):
        orders = orders.filter(content__icontains=cleanData['content'])
    
    if cleanData.get('author', ''):
        orders = orders.filter(author__username=cleanData['author'])
        
    if cleanData.get('checkout', '') == 'on' and cleanData.get('non_checkout', '') == 'on':
        orders = orders
    elif cleanData.get('checkout', '') == 'on':
        orders = orders.filter(checkout=True)
    elif cleanData.get('non_checkout', '') == 'on':
        orders = orders.filter(checkout=False)
    
    monthNum = cleanData.get('month', '1')   
    try:
        monthNum = int(monthNum)
    except Exception as _e:
        monthNum = 1

    if monthNum > 0:
        endDate = datetime.date.today()
        startDate = endDate - monthdelta(monthNum)
        orders = orders.filter(date__range=[startDate, endDate])
    orders = orders.order_by('-date','-id')
    return orders, monthNum

@login_required
def _filterCompany(request,cleanData): 
    companys = Company.objects
    operators = _getOperators()     
    if request.user not in operators:
        return HttpResponseRedirect('/')      
    if cleanData.get('name', ''):
        companys = companys.filter(name__icontains=cleanData['name'])
    if cleanData.get('contact', ''):
        companys = companys.filter(contact__icontains=cleanData['contact'])
    companys = companys.order_by('-id')
    return companys

def ModelToList(order_list):
    try: 
        ids = [i.id for i in order_list ]
        authors = [i.author.username for i in order_list ]
 
        dates = [str(i.date) for i in order_list]
         
        names = [i.company.name for i in order_list]    
        types = [u'制作' if i.type == 'Manufacture' else i.type for i in order_list ]
        contents = [i.content for i in order_list ]
        materials = ['-' if i.type != 'Manufacture' else \
                     str(i.material).decode('UTF-8') + ' (' +str(i.priceMaterial) + \
                     ' * '+str(i.sizeHeight) + ' * '+str(i.sizeWidth) + ')'  for i in order_list ]            
        prices = [i.price for i in order_list ]
        quantitys = [i.quantity for i in order_list ]
        taxPercents = [i.taxPercent for i in order_list ]
        priceIncludeTaxs = [i.priceIncludeTax for i in order_list ]
        checkouts = [u'已完成' if i.checkout else u'未结算' for i in order_list ]
        return [ids, authors, dates, names, types, contents, materials, \
            prices, quantitys, taxPercents, priceIncludeTaxs, checkouts, ] 
    except Exception as _e:       
        return []   

def convertxlsx(order_list, filePath):    
    headings = ['ID',u'记录人',u'日期',u'公司',u'类型',u'内容',u'材料',\
                u'单价',u'数量',u'税率',u'含税价',u'结算']
    data_list = ModelToList(order_list)
    return ListToXlsx(data_list, headings, filePath)

@login_required
def makexlsx(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/')
    
    cleanData = request.POST.dict()
    orders, _monthNum = _filterOrder(request, cleanData)
    order_list = orders.order_by('-date','-id')

    downFilePath = r'Orders-%s.xlsx' % (datetime.datetime.now().strftime('%Y%m%d'),)
    tempDir = tempfile.mkdtemp() 
    tempFilePath = os.path.join(tempDir, '%s.xlsx' % uuid.uuid4().hex)    
    if convertxlsx(order_list, tempFilePath):           
        return downLoadFile(tempFilePath,downFilePath)       
    return HttpResponseRedirect(r'/account/billing/')

@login_required
def addBilling_vue(request):
    operators = _getOperators()
    if request.user not in operators or request.method != 'POST':
        return HttpResponseRedirect('/')    
    cleanData = request.POST.dict()

    company = Company.objects.get(name=cleanData['company'])
    type = cleanData.get('type', '')
    if type not in [i[0] for i in Order.ORDER_TYPE]:
        type = 'Design'
    if type in ['Design', 'Other']:
        price = float(cleanData.get('price', ''))
    count = float(cleanData.get('count', '1'))
    taxPercent = cleanData.get('taxPercent', Order.ORDER_TAX[0][0])
    taxPercent = int(taxPercent)
    if taxPercent not in [int(i[0]) for i in Order.ORDER_TAX]:
        taxPercent = Order.ORDER_TAX[0][0]
    taxPercent = int(taxPercent)     
    o = Order()
    o.company = company
    o.type = type
    o.content = cleanData.get('content', '')     
    reCmp = re.compile('(\d+(\.\d+)?)')
    if type == 'Manufacture':
        material = Material.objects.get(name=cleanData['material'])
        o.material = material
         
        try:
            sizeHeight = reCmp.search(cleanData.get('sizeHeight', ''))
            sizeHeight = float(sizeHeight.groups()[0])
        except Exception as _e:
            sizeHeight = 1
        o.sizeHeight = sizeHeight
         
        try:
            sizeWidth = reCmp.search(cleanData.get('sizeWidth', ''))
            sizeWidth = float(sizeWidth.groups()[0])
        except Exception as _e:
            sizeWidth = 1
        o.sizeWidth = sizeWidth
         
        o.price = sizeHeight * sizeWidth * material.price
    else:
        o.price = price
    o.author = request.user
    o.quantity = count
    o.taxPercent = taxPercent
    o._autoFill()
    o.save()      
    return HttpResponseRedirect('/account/billing_vue/')

@login_required
def addCustomer_vue(request):
    operators = _getOperators()    
    if request.user not in operators or request.method != 'POST':
        return HttpResponseRedirect('/')
    cleanData = request.POST.dict()    
    customerGroup = Group.objects.get(name='Customer')    
    id = User.objects.all().last().id + 1
    username = 'cx%06d' % id
    user = User.objects.create_user(username=username, password='1234qazx')
    user.is_staff = True
    user.is_superuser = False
    user.groups.add(customerGroup)
    user.save()  
    user = User.objects.get(username=username)    
    c = Company()
    c.name = cleanData['name']
    c.taxNumber = cleanData['tax_number']
    c.address = cleanData['address']
    c.bank = cleanData['bank']
    c.bankAccount = cleanData['account']
    c.contact = cleanData['contact']
    c.telephone = cleanData['telephone']
    c.username = user
    c.save()    
    return HttpResponseRedirect('/account/customer_vue/')

#-------------------Rest_Framework---------------------#
from rest_framework.views import APIView,Response,View
from rest_framework import viewsets,pagination
from rest_framework.decorators import detail_route, list_route
from .serializers import UserSerializer, CompanySerializer, MaterialSerializer, OrderSerializer
# #这里，不支持的带页的路由  router.register(r'orders/(?P<page>\d*)?$', views.OrderViewSet)   
#有分页http://localhost:8000/account/materials
class MaterialViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    @list_route()
    #不分页 http://localhost:8000/account/materials/apiall
    def apiall(self, request): 
        material_list = Material.objects.all()
        serializer = MaterialSerializer(material_list, many=True)
        return Response(serializer.data)

#有分页http://localhost:8000/account/companys
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all() 
    serializer_class = CompanySerializer
    @list_route()
    #不分页 http://localhost:8000/account/companys/apiall
    def apiall(self, request): 
        company_list = Company.objects.all()
        serializer = CompanySerializer(company_list, many=True)
        return Response(serializer.data)

# http://127.0.0.1:8000/account/orderlist/
#数据库 序列化API http://localhost:8000/account/orderlist/?author=&company=&content=&format=json&month=2
class Orderlist(APIView): 
    @method_decorator(login_required(login_url='/login/'))
    def get(self,request):        
        orders, monthNum = _filterOrder(request, request.GET.dict())                                
        p1 = MyFormatResultsSetPagination() # 自定义分页
        orders = p1.paginate_queryset(queryset=orders, request=request, view=self) 
        order = OrderSerializer(instance=orders, many=True)         
        return p1.get_paginated_response(order.data) 

#数据库 序列化API http://127.0.0.1:8000/account/customerlist/
class customerlist(APIView): 
    @method_decorator(login_required(login_url='/login/'))
    def get(self,request,*args,**kwargs):
        compans = _filterCompany(request,request.GET.dict())                        
        p1 = MyFormatResultsSetPagination() # 自定义分页
        compans = p1.paginate_queryset(queryset=compans,request=request, view=self) 
        compan = CompanySerializer(instance=compans, many=True) 
        return p1.get_paginated_response(compan.data) 
    
@login_required
#特殊要求的API http://localhost:8000/account/api/
def api(request):
    operators = _getOperators()     
    cleanData = request.GET.dict()
    cleanData = deldictNULL(cleanData)
    page = cleanData.get('page', '1')  
    queryString = '&'.join(['%s=%s' % (k,v) for k,v in cleanData.items() ])    
    orders, monthNum = _filterOrder(request, cleanData)      
    TotalTax = sum(orders.values_list('priceIncludeTax', flat=True))
    operators = [str(o) for o in operators] #数据库记录      
    username = request.user.username    
    mdict = dict()
    if username in operators: #如果登录用户在Operator组
         type_list = [i[0] for i in Order.ORDER_TYPE]
         taxPercent_list = [i[0] for i in Order.ORDER_TAX]      
         mdict = {'type_list':type_list,'taxPercent_list':taxPercent_list}          
    mydict = {  'operators':operators,'monthNum':monthNum,\
               'cleanData':cleanData,'queryString':queryString,\
               'username':username,'TotalTax' : TotalTax,'PAGE_NUM':PAGE_NUM}     
    mydict.update(mdict)
    return JsonResponse(mydict)

# http://localhost:8000/account/billing_vue/?page=1
@login_required
def billing_vue(request): 
    queryString ='&'.join(['%s=%s' % (k,v) for k,v in request.GET.dict().items()])   
    print('queryString0 =',queryString )
    return render(request, 'account/billing_vue.html', context=locals())


# http://localhost:8000/account/customer_vue/
@login_required   
def customer_vue(request):
    queryString ='&'.join(['%s=%s' % (k,v) for k,v in request.GET.dict().items()])   
    return render(request, 'account/customer_vue.html', context=locals())
