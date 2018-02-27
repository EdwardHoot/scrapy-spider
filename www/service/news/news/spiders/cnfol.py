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

class CnfolSpider(CrawlSpider):
    name='cnfol'
    source = "中金在线"
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday

    def start_requests(self):
        start_urls = [
            'http://app.cnfol.com/test/newlist_api.php?catid=1603&callback=callback&_=1486446304954&page=',
            'http://app.cnfol.com/test/newlist_api.php?catid=1280&callback=callback&_=1486446004127&page=',
            'http://app.cnfol.com/test/newlist_api.php?catid=1591&callback=callback&_=1486446376465&page=',
            'http://app.cnfol.com/test/newlist_api.php?catid=1277&callback=callback&_=1486446401495&page=',
            'http://app.cnfol.com/test/newlist_api.php?catid=1609&callback=callback&_=1486446531502&page='
        ]
        requests=[]
        for url in start_urls:
            request1 = Request(url+'1', callback=self.parse_json)
            request2 = Request(url+'2', callback=self.parse_json)
            # for i in range(2):
            #     request = Request(url + i, callback=self.parse_json)
            requests.append(request1)
            requests.append(request2)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_json(self, response):
        jsonBody = json.loads(response.body[9:-1].decode('utf-8', errors='ignore').encode('utf-8'))
        for reccord in jsonBody:
            if self.yesterday in reccord['Url']:
                yield Request(reccord['Url'], callback=self.parse_news)

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
        title=response.xpath('//*[@id="Title"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        p = response.xpath('//div[@id="Content"]')
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
