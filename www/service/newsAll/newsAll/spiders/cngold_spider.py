#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class CngoldSpider(CrawlSpider):
    name='cngold'
    source = "中金网"
    allowed_domains = ["cngold.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://news.cngold.com.cn/gjdt.html',
        'http://news.cngold.com.cn/gjdt_2.html',
        'http://news.cngold.com.cn/gjdt_3.html',
        'http://news.cngold.com.cn/gjdt_4.html',
        'http://news.cngold.com.cn/gnxw.html',
        'http://news.cngold.com.cn/zhaiq.html',
        'http://www.cngold.com.cn/zjsd/zjsd.html',
        'http://news.cngold.com.cn/guojqh.html',
        'http://news.cngold.com.cn/gjqh.html',
        'http://gold.cngold.com.cn/hjyw.html',
        'http://gold.cngold.com.cn/hjyw_2.html',
        'http://gold.cngold.com.cn/hjyw_3.html',
        'http://forex.cngold.com.cn/whxw.html',
        'http://forex.cngold.com.cn/whxw.html_2',
        'http://forex.cngold.com.cn/whxw.html_3',
        'http://forex.cngold.com.cn/whxw.html_4'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        # Rule(LinkExtractor(allow='/_[0-9].html'))
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
        title=response.xpath('//div[@class="right_area2"]/h1/text()').extract()
        if not title:
            title = response.xpath('//div[@class="right_area"]/h1/text()').extract()
        if title:
            item['title']=title
    def get_date(self,response,item):
        date=response.xpath('//div[@class="right_in2"]/text()').extract()[0]
        if date:
            item['date']=''.join(date).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="left_body_center"]/p')
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
