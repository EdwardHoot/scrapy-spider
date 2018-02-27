#encoding: utf-8
import scrapy
import re
import uuid
import datetime,time
import json
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request

class WallstreetSpider(CrawlSpider):
    name='wallstreet'
    source = "华尔街见闻"
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday

    def start_requests(self):
        start_urls = [
            'https://api.wallstreetcn.com/v2/pcarticles?limit=50&category=most-recent&articleCursor=1486547805'
        ]
        requests=[]
        for url in start_urls:
            request = Request(url, callback=self.parse_json)
            requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_json(self, response):
        jsonBody = json.loads(response.body.decode('utf-8', errors='ignore').encode('utf-8'))
        datas=jsonBody['posts']
        for data in datas:
            create_time = time.localtime(float(data['resource']['createdAt']))
            timeStr = time.strftime("%Y%m%d",create_time)
            if self.yesterday in timeStr:
                yield Request(data['resource']['url'], callback=self.parse_news)

    def parse_news(self,response):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        self.get_source(response,item)
        self.get_title(response,item)
        self.get_date(response,item)
        self.get_body(response,item)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!remenber to Retrun Item after parse
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
        title=response.xpath('//div[@class="title-text"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@class="title-meta-time"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        p = response.xpath('//div[@class="page-article-content"]')
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
