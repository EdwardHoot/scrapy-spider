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

class HexunSpider(CrawlSpider):
    name='hexun'
    source = "和讯网"
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    reg=yesterday

    def start_requests(self):
        start_urls = [
            'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=108511056&s=100&priority=0',
            'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=181133690&s=100&priority=0',
            'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=100018982&s=100&priority=0',
            'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=108511812&s=100&priority=0',
            'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=100018983&s=100&priority=0',
            'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=125270156&s=100&priority=0'
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
        result = jsonBody['result']
        for url in result:
            if self.yesterday in url['entityurl']:
                yield Request(url['entityurl'], callback=self.parse_news)

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
        title=response.xpath('//div[@class="layout mg articleName"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="pr20"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'')
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="art_contextBox"]/p')
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
