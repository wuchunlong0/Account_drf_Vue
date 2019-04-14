account_drf_vue_py354_dj21    2018.11.18 <br>
1、外键使用 drf方式  <br>
2、mybtn.css 分页按钮通用,此模块不会与模块其他发生冲突!<br>
3、改变模板 时间显示：<br> 
<td><span> {[ i.date.substring(0,10)+' '+i.date.substring(11,19)]} </span></td><br>
效果：2018-11-17 11:09:38<br>

./start.sh -i<br>
admin/1234qazx     op0/1234qazx  cx0/1234qazx<br>

管理 http://localhost:8000/admin/<br>
主页 http://localhost:8000/<br>

分页 http://localhost:8000/account/materials<br>
不分页 http://localhost:8000/account/materials/apiall<br>

有分页 http://localhost:8000/account/companys<br>
不分页 http://localhost:8000/account/companys/apiall<br>

自定义分页 http://127.0.0.1:8000/account/orderlist/<br>
自定义分页 http://127.0.0.1:8000/account/customerlist/<br>

特殊要求的API http://localhost:8000/account/api/<br>