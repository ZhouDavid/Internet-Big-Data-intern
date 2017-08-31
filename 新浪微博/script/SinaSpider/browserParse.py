#coding:utf-8
import re
import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains


# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] =('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36')
driver = webdriver.PhantomJS(executable_path='E:\phantomjs-2.1.1-windows\\bin\phantomjs.exe')
wait = ui.WebDriverWait(driver,10)
#driver = webdriver.Chrome('E:/chromedriver.exe')

def LoginWeibo(username,password):
	# driver.maximize_window()
	# print(driver.get_window_size())

	driver.get('https://weibo.cn/pub/')
	login_tag = driver.find_element_by_xpath('//a[@href="http://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt="]')
	login_tag.click()
	

	user_tag = driver.find_element_by_xpath('//input[@id="loginName"]')
	pw_tag = driver.find_element_by_xpath('//input[@id="loginPassword"]')
	pw_tag.send_keys(password)
	submit_tag = driver.find_element_by_xpath('//a[@id="loginAction"]')
	#submit_tag.click()
	#time.sleep(2)
	#print(driver.current_url)
	#driver.get('https://m.weibo.cn/status/F9bYR9GcT')
def enterWeibo(url):
	driver.get(url)
	repost_tag = driver.find_elements_by_xpath('//a[@class="comment-tab"]')[0]
	repost_tag.click()
	time.sleep(5)
	res = requests.get('https://m.weibo.cn/api/statuses/repostTimeline?id=4121910092307199&page=2')
	print(res.text)
	#print(repost_tag.get_attribute('innerHTML'))

	open('tmp','w',encoding='utf-8').write(driver.page_source)

def parseRepost(url):
	session = requests.session()
	data = json.loads(session.get(url).text)['data']
	return data

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_decode(string, alphabet=ALPHABET):
    base = len(alphabet)
    strlen = len(string)
    num = 0
    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num
def str2uid(code):
	code1 = code[0]
	code2 = code[1:5]
	code3 = code[5:]

	id1 = base62_decode(code1)
	id2 = base62_decode(code2)
	id3 = base62_decode(code3)
	numList = [id1, id2, id3]
	uid = ''.join(map(str, numList))
	return uid
if __name__ == '__main__':
	#LoginWeibo('18810918292','498072205')
	# url='https://m.weibo.cn/status/F9bYR9GcT'
	# enterWeibo(url)
	code = 'F9bYR9GcT'
	url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=4121910092307199&page=1'
	commentList = parseRepost(url)
	msg = commentList
	# for comment in commentList:
	# 	if comment['user']['screen_name'] == '白老三啊':
	# 		print(comment)
	# url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F%3Fluicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home&backTitle=%CE%A2%B2%A9&vt='
	# res = requests.get(url,headers = {'User-agent': 'spider'})
	# open('E:/page6.html','w',encoding='utf-8').write(res.text)