# -*- coding: utf-8 -*-
# modelAPI.py  2018.10.16  问题：如何做单元测试？？？ addlist为做单元测试而设置。
from __future__ import unicode_literals
"""
model.objects.values()能够以列表字典形式，获得数据库字段值，字段有外键时，只能获得:字段_id
 该函数以列表字典形式，获得数据库字段值，也可以获得外键字段值。
 models_values数据库列表字典形式:[{'字段1':'1','字段2':'2',...},{'字段1':'11','字段2':'22',...}, ...]
 listdict=[{'字段名': 外键数据库名}, ...]。例如Account项目 外键：[dict(author=User),dict(company=Company),dict(material=Material)]
 测试在：http://localhost:8888/test/uikit_page2/
"""
def get_model_values(models_values,listdict):    
    try:                                     
        for T in models_values:
            adddict = {}                         
            for k,v in T.items():
                for (index,d) in enumerate(listdict):                                        
                    for k1,v1 in d.items():
                        if k == k1 + '_id':
                            adddict.update({k1 : str(v1.objects.get(id=v)) }) if v else adddict.update({k1 :v})                                                      
                            if index == 0:
                                adddict.update(T)
            yield adddict 
                                                                                                                       
    except Exception as ex:
        print("get_model_listdict() err!"  + str(ex))
        yield  {}


#外键 由列表中某个元素获得下标。数据库名model，值value  测试：http://localhost:8888/accountTest/str_get_id/
def get_model_id(model,field,value):
    models = list(model.objects.values_list(field,flat=True)) #列表
    print('models===',models)
    try:
        
        id = models.index(value) 
    except Exception as ex:
        id = 0
        print('#####')
        
    return  id#返回列表中某个元素的下标