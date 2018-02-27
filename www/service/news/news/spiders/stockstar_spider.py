#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class StockstarSpider(CrawlSpider):
    name='stockstar'
    source = "证券之星"
    allowed_domains = ["stockstar.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = ['http://www.stockstar.com/roll/finance.shtml',
                  'http://www.stockstar.com/roll/bond.shtml',
                  'http://house.stockstar.com/list/3307.shtml',
                  'http://house.stockstar.com/list/3293.shtml',
                  'http://focus.stockstar.com/list/4827.shtml',
                  'http://focus.stockstar.com/list/4829.shtml',
                  'http://focus.stockstar.com/list/4915.shtml',
                  'http://finance.stockstar.com/list/1221.shtml',
                  'http://finance.stockstar.com/list/955.shtml',
                  'http://finance.stockstar.com/list/2921.shtml',
                  'http://finance.stockstar.com/list/2437.shtml',
                  'http://finance.stockstar.com/list/2457.shtml',
                  'http://finance.stockstar.com/list/1119.shtml',
                  'http://finance.stockstar.com/list/2863.shtml',
                  'http://finance.stockstar.com/list/1765.shtml',
                  'http://finance.stockstar.com/list/2861.shtml',
                  'http://finance.stockstar.com/list/947.shtml',
                  'http://finance.stockstar.com/list/1117.shtml',
                  'http://finance.stockstar.com/list/2859.shtml']
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        # Rule(LinkExtractor(allow='_[0-9]+.html'))
    )
    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')
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
        title=response.xpath('//div[@id="container-box"]/h1/text()').extract()
        if title:
            item['title']=title
    def get_date(self,response,item):
        date=response.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        if date:
            item['date']=''.join(date).replace('-','').replace(':','').replace(' ','')
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="container-article"]/p')
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
