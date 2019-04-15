# -*- coding: UTF-8 -*-
# 删除字典中value为空的键值对方法
def deldictNULL(mydict):
    for key in list(mydict.keys()):
        if not mydict.get(key):
            del mydict[key]
    return mydict