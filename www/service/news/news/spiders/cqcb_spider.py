#encoding: utf-8
import scrapy
import re
import uuid
import datetime
import json
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request

class CqcbSpider(CrawlSpider):
    name='cqcb'
    source = "重庆晨报"
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    year=yesterday.strftime('%Y')
    yesterday = yesterday.strftime('%Y-%m-%d')

    reg=yesterday

    def start_requests(self):
        start_urls = [
            'http://source.cqcb.com/finance/index'
        ]
        requests=[]
        for url in start_urls:
            requests.append(Request(url + '.json', callback=self.parse_json))
            # for i in range(2,10):
            #     request = Request(url + i, callback=self.parse_json)
            #     requests.append(request1)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_json(self, response):
        jsonBody = json.loads(response.body.decode('utf-8', errors='ignore').encode('utf-8'))['newslist']
        for reccord in jsonBody:
            if self.yesterday in reccord['titleurl']:
                yield Request('http://source.cqcb.com'+reccord['titleurl'], callback=self.parse_news)

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
        title=response.xpath('//div[@class="ftop_biaoti"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@class="ftop_biaoti"]/h2/span[1]/text()').extract()
        if date:
            item['date']=self.year+''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
    def get_body(self,response,item):
        p = response.xpath('//div[@class="farticle_text"]')
        news_body = ''
        # for p in paras:
        data = p.xpath('string(.)').extract()
        if data:
            body = ''
            for line in ''.join(data).splitlines():
                #   print entry.encode('utf-8')
                body += line.strip()
            news_body += body + '_|_'
        item['body'] = news_body.replace('_|__|_','_|_')
