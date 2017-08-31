#coding:utf-8
import requests
import selenium
import chardet
# r = requests.get('http://weibo.com/1564562957/FgWECAdT0')
# file = open('test.txt','wb')
# text = r.text
# text = text.encode('utf-8')
# file.write(text)
#print(r.text)


# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# class PythonOrgSearch(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome('E:\chromedriver.exe')

#     def test_search_in_python_org(self):
#         driver = self.driver
#         driver.get("https://weibo.com/1644461042/Fh4dmwEbg?")
#         text = driver.page_source
#         file = open('text','w')
#         file.write(text)
#         #self.assertIn("Python", driver.title)
#         # elem = driver.find_element_by_name("q")
#         # elem.send_keys("pycon")
#         # elem.send_keys(Keys.RETURN)
#         #assert "No results found." not in driver.page_source

#     def tearDown(self):
#         self.driver.close()

# if __name__ == "__main__":
#     unittest.main()


import requests
import re
import json
import urllib
import base64
import rsa
import binascii

user_agent = {'User-agent': 'spider'}

username = '18810918292'
password = '498072205'

prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)' % username
login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'
session = requests.Session()
info = session.get(prelogin_url)
start = info.text.find('{')
end = info.text.find(')')
info = re.findall(r'(?<=\().*(?=\))',info.text)[0]
data = json.loads(info)
#加密用户名
username = urllib.parse.quote(username)
username = base64.encodestring(username.encode('utf-8'))[:-1]

rsakv = data['rsakv']
servertime = data['servertime']
nonce = data['nonce']
pubkey = data['pubkey']

#加密密码
rsaPublicKey = int(pubkey,16)
key = rsa.PublicKey(rsaPublicKey,65537)
message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
passwd = rsa.encrypt(message.encode('utf-8'), key) #加密
passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。

#构造请求头信息
postData= {
	'entry': 'weibo',\
	'gateway': '1',\
	'from': '',\
	'savestate': '7',\
	'userticket': '1',\
	'ssosimplelogin': '1',\
	'vsnf': '1',\
	'vsnval': '',\
	'su': username,\
	'service': 'miniblog',\
	'servertime': servertime,\
	'nonce': nonce,\
	'pwencode': 'rsa2',\
	'sp': passwd,\
	'encoding': 'UTF-8',\
	'prelt': '115',\
	'rsakv' : rsakv,\
	'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',\
	'returntype': 'META'\
}

response = session.post(login_url,data=postData)
login_url = re.findall(r'http://weibo.*&retcode=0',response.text)[0]
response = session.get(login_url)
cookies = response.cookies

# uid = re.findall(r'"uniqueid":"(\d+)",',response.text)[0]
# url = "http://weibo.com/u/"+uid

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] =('spider')

#options = webdriver.ChromeOptions()
#ptions.add_argument('user-agent="spider"')
#browser = webdriver.Chrome('E:\chromedriver.exe',chrome_options=options)
#browser = webdriver.PhantomJS(r'C:\\Users\\ZhouJianyu\\Downloads\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',desired_capabilities=dcap)
url = 'https://m.weibo.cn/status/F9bYR9GcT'

response = session.get(url)
text = response.text
open('tmp','w',encoding='utf-8').write(text)


# r = requests.get("http://weibo.com/3261134763/F9bYR9GcT?from=page_1006053261134763_profile&wvr=6&mod=weibotime&type=repost",headers=user_agent)
# text = r.text
# text = text.encode('utf-8')
# file = open('test','wb')
# file.write(text)
# print(r.url)
