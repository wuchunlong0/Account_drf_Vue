account_drf_vue_py354_dj21    2018.11.18
1、外键使用 drf方式  
2、mybtn.css 分页按钮通用,此模块不会与模块其他发生冲突!
3、改变模板 时间显示： 
<td><span> {[ i.date.substring(0,10)+' '+i.date.substring(11,19)]} </span></td>
效果：2018-11-17 11:09:38

./start.sh -i
admin/1234qazx     op0/1234qazx  cx0/1234qazx

管理 http://localhost:8000/admin/
主页 http://localhost:8000/

分页 http://localhost:8000/account/materials
不分页 http://localhost:8000/account/materials/apiall

有分页 http://localhost:8000/account/companys
不分页 http://localhost:8000/account/companys/apiall

自定义分页 http://127.0.0.1:8000/account/orderlist/
自定义分页 http://127.0.0.1:8000/account/customerlist/

特殊要求的API http://localhost:8000/account/api/