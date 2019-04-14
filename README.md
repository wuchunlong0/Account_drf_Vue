Python3.54  Django2.1<br>
account_py3_dj21<br><br>
外键使用， 不用特别处理，模板就能渲染。<br>


一、功能：<br>
高域传媒<br>

二、相关技术<br>
（一）时间格式<br>

1、设置环境（中国时区）：settings.py<br>
LANGUAGE_CODE = 'zh-Hans'<br>
TIME_ZONE = 'Asia/Shanghai'<br>

2、models.py<br>
date = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)<br>

3、views.py<br>
o = Order()<br>
o.date = datetime.datetime.now()-datetime.timedelta(days=random.randint(1, 500))<br>
o.save()<br>

4、前端 html输出格式：<br>
{{ i.date }} 2018年11月15日 10:26<br>
{{ i.date | date:"Y-m-d H:i:s" }}   2018-11-15 10:26:44<br>


