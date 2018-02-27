#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class PeopleSpider(CrawlSpider):
    name='people'
    source = "人民网"
    allowed_domains = ["people.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y/%m%d')
    reg=yesterday
    start_urls = [
        'http://finance.people.com.cn/GB/70846/index.html',
        'http://finance.people.com.cn/GB/153179/153180/index.html',
        'http://finance.people.com.cn/GB/1045/index.html',
        'http://finance.people.com.cn/GB/153179/153522/index.html',
        'http://finance.people.com.cn/GB/153179/153480/index.html',
        'http://finance.people.com.cn/GB/71364/index.html',
        'http://finance.people.com.cn/stock/GB/222942/index.html',
        'http://finance.people.com.cn/stock/GB/220477/index.html',
        'http://finance.people.com.cn/stock/GB/68055/index.html',
        'http://finance.people.com.cn/stock/GB/220485/index.html',
    ]
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        # Rule(LinkExtractor(allow='/index[2-4].html'))
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
        title=response.xpath('//h1/text()').extract()
        if title:
            item['title']=title
    def get_date(self,response,item):
        date=response.xpath('//div[@class="fl"]/text()').extract()[0]
        if date:
            item['date']=''.join(''.join(date).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()[:12])+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="rwb_zw"]/p')
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
