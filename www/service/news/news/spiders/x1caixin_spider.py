#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request

class X1caixinSpider(CrawlSpider):
    name='1caixin'
    source = "财信网"
    allowed_domains = ["1caixin.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday

    def start_requests(self):
        start_urls = [
            'http://www.1caixin.com.cn/list-69.html',
            'http://www.1caixin.com.cn/list-70.html',
            'http://www.1caixin.com.cn/list-71.html',
            'http://www.1caixin.com.cn/list-62.html',
            'http://www.1caixin.com.cn/list-63.html',
            'http://www.1caixin.com.cn/list-64.html',
            'http://www.1caixin.com.cn/list-66.html',
            'http://www.1caixin.com.cn/list-67.html',
            'http://www.1caixin.com.cn/list-68.html',
            'http://www.1caixin.com.cn/list-77.html',
        ]
        base_urls = [
            'http://www.1caixin.com.cn/list_69_',
            'http://www.1caixin.com.cn/list_70_',
            'http://www.1caixin.com.cn/list_71_',
            'http://www.1caixin.com.cn/list_62_',
            'http://www.1caixin.com.cn/list_63_',
            'http://www.1caixin.com.cn/list_64_',
            'http://www.1caixin.com.cn/list_66_',
            'http://www.1caixin.com.cn/list_67_',
            'http://www.1caixin.com.cn/list_68_',
            'http://www.1caixin.com.cn/list_77_',
        ]
        requests = []
        for url in start_urls:
            request = Request(url, callback = self.parse_page)
            requests.append(request)
        for url in base_urls:
            # for i in range(2,30):
            for i in range(2,3):
                request = Request(url + str(i)+'.html', callback=self.parse_page)
                requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self, response):
        news = response.xpath('//li')
        for p in news:
            date = ''.join(p.xpath('span[@class="date_1"]/text()').extract()).replace(u'年', u'').replace(u'月', u'').replace(u'日', u'').replace(u':', u'').replace(u' ', u'').strip() + '00'
            if self.yesterday in date:
                link = 'http://www.1caixin.com.cn'+''.join(p.xpath('a/@href').extract())
                yield Request(link, callback=lambda response, date_=date: self.parse_news(response, date_))


    def parse_news(self,response,date_):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        self.get_source(response, item)
        self.get_title(response, item)
        item['date'] = date_
        self.get_body(response,item)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!remenber to Retrun Item after parse
        if item['body']:
            return item

    def get_id(self,response,item):
        id=uuid.uuid4()
        if id:
            item['id']=id
    def get_url(self,response,item):
        news_url=response.url
        if news_url:
            item['url']=news_url
    def get_source(self,response,item):
        source=self.source
        if source:
            item['source']=source
    def get_title(self,response,item):
        title=response.xpath('//div[@class="tthd"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="article"]/p')
        news_body = ''
        for p in paras:
            data = p.xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    #   print entry.encode('utf-8')
                    body += line.strip()
                news_body += body + '_|_'
        item['body'] = news_body.replace('_|__|_','_|_')
