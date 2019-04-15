# -*- coding: utf-8 -*-
# pageAPI.py  分页类
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
PAGE_NUM = 25 #每页显示数
def toInt(c):
    try:
        i = int(c)
    except Exception as _e:
        i = 1
    return i
# 使用该函数步骤：2018.03.21
# 一、拷入文件：static/home/css/btn.css     templates/home/djangopage.html
# 二、在视图文件中
# 1、引用： from myAPI.pageAPI import djangoPage,PAGE_NUM,toInt
# 2、方法：def show(request):  -->   def show(request, page):
# 3、在返回html前台以前加入下列两条语句，其中blogs数据库记录或列表。
#      blog_list, pageList, paginator, page = djangoPage(blogs,page,PAGE_NUM)  #调用分页函数
#      offset = PAGE_NUM * (page - 1)
# 4、在html前台文件中加入分布：<div style="padding-left:520px;"">{% include 'home/djangopage.html' %}  </div> <!--分页--> 
# 三、更改路由：r'^show/'      -->        r'^show/(?P<page>\d*)?$'
#适用django分页  1、contact_list数据库记录或列表；2、page当前页；3、设置每页显示数 num
# 综合应用实例：http://localhost:8000/accountTest/billing/
def djangoPage(contact_list,page,num):
    paginator = Paginator(contact_list, num) 
    page = toInt(page) 
    try:
        model_list = paginator.page(page)
    except PageNotAnInteger:
        model_list = paginator.page(1)
    except EmptyPage:
        model_list = paginator.page(paginator.num_pages)         
    pageList = list(paginator.page_range)
    if page < (paginator.num_pages)-3:
        pageList[page+2:-1] = ['...']
    if page > 1+3:
        pageList[1:page-3] = ['...']        
    
    return model_list,pageList,paginator.num_pages,page

from rest_framework.pagination import PageNumberPagination #分页
from rest_framework.response import Response
class MyFormatResultsSetPagination(PageNumberPagination): 
    page_size_query_param = "page_size"
    page_query_param = 'page'
    page_size = PAGE_NUM
    max_page_size = 10000
        
    """
    自定义分页方法 依赖 settings.py设置 'ReturnList' object has no attribute 'GET'
    """ 
    def get_paginated_response(self,data):
        page = self.page.start_index() // self.page.paginator.per_page + 1
        count = self.page.paginator.count #总数
        page_size = self.page.paginator.per_page #每页数
        data_list, pageList, num_pages, page = djangoPage(range(count),page,PAGE_NUM)  #调用分页函数
        """
        设置返回内容格式
        """
        return Response({'results': data, 
                        'pagination': count, 
                        'page_size': page_size, 
                        'page': page,
                        'num_pages' : num_pages,
                        'pageList':pageList})
