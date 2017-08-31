# -*- coding:utf-8 -*-
import requests
import json
import re
import os
import gevent
import time
import random
import urllib
import base64
import rsa
import binascii
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
class CommentCrawl(object):
    '''
    用来爬取新浪微博评论数据
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Cookie': 'SINAGLOBAL=7760669112226.401.1481772111468; UM_distinctid=15aa349569f19-0c778aad0b69cb-414a0229-100200-15aa34956a0ac; SSOLoginState=1492570145; _s_tentry=-; Apache=948140024978.4543.1492570202501; ULV=1492570202834:103:13:3:948140024978.4543.1492570202501:1492481157923; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295; TC-V5-G0=b8dff68fa0e04b3c8f0ba710d783479a; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; wvr=6; UOR=,,www.liaoxuefeng.com; SCF=AjVnYn5w5MVRKBChxLVFcVRWP9YlRAZbNSb6l1VItKaZjaF0ROvTFLx0asLdajQthg4DBw-fD38Zh5D7Eoh_8i4.; SUB=_2A251812VDeRhGeVM6lIU8izEwjyIHXVWichdrDV8PUJbmtAKLXnHkW9G52j5C_LYFrXp0ibisjLZH7NYQw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhQMFyM94ynlSl9JBZenkS15JpX5o2p5NHD95Q0eo27SKzE1h.7Ws4DqcjZxPiDqcj_K2v1x7tt; SUHB=0P1M-fknKXkPe0; ALF=1524106144; WBStorage=02e13baf68409715|undefined'}
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    all_comment = []
    def __init__(self,urlll,file_name):
        self.urlll = urlll
        self.file_name=file_name
        user_agent = {'User-agent': 'spider'}

        username = '18810918292'
        password = '498072205'

        prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)' % username
        login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'
        self.session = requests.Session()
        info = self.session.get(prelogin_url)
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
        
        response = self.session.post(login_url,data=postData)
        login_url = re.findall(r'http://weibo.*&retcode=0',response.text)[0]
        response = self.session.get(login_url)

    def base62_decode(self,string, alphabet=ALPHABET):
        base = len(alphabet)
        strlen = len(string)
        num = 0
        idx = 0
        for char in string:
            power = (strlen - (idx + 1))
            num += alphabet.index(char) * (base ** power)
            idx += 1
        return num

    def parser_url(self):
        code = self.urlll.split('?')[0].split('/')[-1]

        code1 = code[0]
        code2 = code[1:5]
        code3 = code[5:]

        id1 = self.base62_decode(code1)
        id2 = self.base62_decode(code2)
        id3 = self.base62_decode(code3)
        numList = [id1, id2, id3]
        plus = ''.join(map(str, numList))
        comment_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id='+ plus +'&root_comment_max_id_type=0&page={}'
        return comment_url
    def get_url_page(self):
        r = self.session.get(self.parser_url().format(1))
        data = json.loads(r.text)
        total_page = data['data']['page']['totalpage']
        return total_page

    def all_urls(self):
        all_urls = [self.parser_url().format(i + 1) for i in range(self.get_url_page())]
        return all_urls

    def comment_parser(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select('.WB_text')
        comment = [i.text.split('：')[-1] for i in data]
        return comment
    def finnal_text(self,url):
        finnal_all_comment=''.join(self.all_comment)
        r1 = self.session.get(url)
        time.sleep(random.randint(1,5))
        data1 = json.loads(r1.text)
        html =data1['data']['html']
        finnal_data = self.comment_parser(html)
        self.all_comment+=finnal_data
        print(finnal_all_comment)
        return finnal_all_comment
    def save_file(self,url):
        path = os.getcwd()
        filename = self.file_name + '.txt'
        file = path + '/' + filename
        f = open(file, 'a+', encoding='utf-8')
        f.write(self.finnal_text(url))

if __name__ == "__main__":
    url = 'https://weibo.com/2101605197/FhXGOd86R?from=page_1005052101605197_profile&wvr=6&mod=weibotime'
    aa = CommentCrawl(url,'小米6发布会')
    all_link = aa.all_urls()
    pool=ThreadPool(4)
    results = pool.map(aa.save_file,all_link)
    pool.close()
    pool.join()