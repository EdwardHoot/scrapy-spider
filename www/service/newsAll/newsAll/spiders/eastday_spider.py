#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class EastdaySpider(CrawlSpider):
    name='eastday'
    source = "东方网"
    allowed_domains = ["eastday.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://finance.eastday.com/stock/jj/',
        'http://finance.eastday.com/stock/gsch/',
        'http://finance.eastday.com/stock/yh/',
        'http://finance.eastday.com/stock/qh/',
        'http://finance.eastday.com/stock/lcal/',
        'http://finance.eastday.com/stock/bx/',
        'http://finance.eastday.com/economic/jjyw/',
    ]
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        Rule(LinkExtractor(allow='index[1-2].html'))
        # Rule(LinkExtractor(allow='index[0-9].html'))
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
        title=response.xpath('//div[@id="biaoti"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        if date:
            item['date']=self.yesterday+''.join(''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()[-6:])
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="zw"]/p')
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
