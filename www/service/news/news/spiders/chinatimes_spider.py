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


class ChinatimeSpider(CrawlSpider):
    name='chinatimes'
    source = "华夏时报网"
    allowed_domains = ["chinatimes.cc"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    ldate=yesterday.strftime('%Y%m%d')
    yesterday = yesterday.strftime('%Y')+yesterday.strftime('%m').replace('0','')+yesterday.strftime('%d').replace('0','')

    def start_requests(self):
        requests = []
        base_urls = [
            'http://www.chinatimes.cc/category/1.html',
            'http://www.chinatimes.cc/category/2.html',
            'http://www.chinatimes.cc/category/3.html',
            'http://www.chinatimes.cc/category/4.html',
            'http://www.chinatimes.cc/category/5.html',
            'http://www.chinatimes.cc/category/6.html',
            'http://www.chinatimes.cc/category/7.html',
            'http://www.chinatimes.cc/category/8.html',
            'http://www.chinatimes.cc/category/9.html'
        ]
        for url in base_urls:
            requests.append(Request(url, callback=self.parse_page))
            # for i in range(1,1500):
            #     requests.append(Request(url+'?page='+str(i),callback=self.parse_page))
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self, response):
        news = response.xpath('//div[@class="item"]')
        for p in news:
            date=''.join(p.xpath('div[@class="info"]/span[@class="time"]/text()').extract()).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
            if date and self.yesterday in date:
                yield Request('http://www.chinatimes.cc'+''.join(p.xpath('h2/a/@href').extract()),callback=self.parse_news)

    def parse_news(self,response):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        self.get_source(response,item)
        self.get_title(response,item)
        self.get_date(response,item)
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
        title=response.xpath('//div[@class="title"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//p[@id="pubtime_baidu"]/text()').extract()
        if date:
            item['date']=self.ldate+''.join(''.join(date).replace(u':',u'').replace(u' ',u'').strip()[-6:])
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="infoMain"]/p')
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