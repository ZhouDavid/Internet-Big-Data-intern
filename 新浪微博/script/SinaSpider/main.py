import scrapy
from scrapy import cmdline
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
import time
from selenium import webdriver

class SinaSpider(CrawlSpider):
    # name of spiders
    name = 'sinaSpider'
    start_urls = ['http://weibo.com/3261134763/F9bYR9GcT?from=page_1006053261134763_profile&wvr=6&mod=weibotime&type=repost']
    user_agent = 'spider'
    def __init__(self):
        CrawlSpider.__init__(self)
        webdriver.PhantomJS()
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent="spider"')
        self.browser = webdriver.Chrome('E:\chromedriver.exe',chrome_options=options)

    def __del__(self):
        self.browser.close()

    def parse(self,response):
        self.browser.get(response.url)
        time.sleep(5)
        result = response.css('title::text').extract()
        html = self.browser.page_source.encode('utf-8')
        open('lyf.html','wb').write(html)
        yield {'title':result}

cmdline.execute('scrapy runspider main.py -o test.csv'.split())