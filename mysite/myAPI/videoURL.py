# -*- coding: utf-8 -*-
import requests
from lxml import etree
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}


video_url_list = ["https://www.jqaaa.com/jx.php?url=", #0
        "https://5.5252e.com/jx/b.php?url=",
        "http://yun.mt2t.com/yun?url=",        
        "http://www.wmxz.wang/video.php?url=",    
        "http://api.bbbbbb.me/yunjx/?url=",        
        "http://000o.cc/jx/ty.php?url=",
        "http://api.baiyug.cn/vip/index.php?url=", #6 le电视剧、爱奇艺
        "http://yun.baiyug.cn/vip/?url=",
];

def parseUrl(url):
    requests.packages.urllib3.disable_warnings()   #python3.5 加这一句OK
    response = requests.get(url,headers=headers) #python2 正常；python3 报错
    if response.status_code == 200:
        return True
    print('err url: ',url)
    return False

import unittest            
class TestfileAPI(unittest.TestCase):        
    def test_XlsxToList_0(self):         
        self.assertEquals(parseUrl(video_url_list[0]),True)
    def test_XlsxToList_1(self):         
        self.assertEquals(parseUrl(video_url_list[1]),True)
    def test_XlsxToList_2(self):         
        self.assertEquals(parseUrl(video_url_list[2]),True)
    def test_XlsxToList_3(self):         
        self.assertEquals(parseUrl(video_url_list[3]),True)
    def test_XlsxToList_4(self):         
        self.assertEquals(parseUrl(video_url_list[4]),True)
    def test_XlsxToList_5(self):         
        self.assertEquals(parseUrl(video_url_list[5]),True)
    def test_XlsxToList_6(self):         
        self.assertEquals(parseUrl(video_url_list[6]),True)
    def test_XlsxToList_7(self):         
        self.assertEquals(parseUrl(video_url_list[7]),True)
#     def test_XlsxToList_8(self):         
#         self.assertEquals(parseUrl(video_url_list[8]),True)
#     def test_XlsxToList_9(self):         
#         self.assertEquals(parseUrl(video_url_list[9]),True)
#     def test_XlsxToList_10(self):         
#         self.assertEquals(parseUrl(video_url_list[10]),True)





if __name__ == '__main__':
    unittest.main()  