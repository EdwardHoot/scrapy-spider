#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class CaijingSpider(CrawlSpider):
    name='caijing'
    source = "财经网"
    allowed_domains = ["caijing.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://industry.caijing.com.cn/industrianews/'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg), callback="parse_news", follow=True),
        Rule(LinkExtractor(allow='industrianews/[2-4].shtml')),
        # Rule(LinkExtractor(allow='industrianews/[0-9].shtml')),
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
        title=response.xpath('//*[@id="cont_title"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()

    def get_date(self, response, item):
        date = response.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        if date:
            item['date'] = ''.join(date).replace(u'-', u'').replace(u':', u'').replace(u' ', u'').strip()
        else:
            date = response.xpath('//span[@id="cont_riqi"]/text()').extract()
            if date:
                item['date'] = ''.join(
                    ''.join(date).replace(u'年', u'').replace(u'月', u'').replace(u'日', u'').replace(u':', u'').replace(
                        u' ', u'').strip()[-12:]) + '00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="the_content"]/p')
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
