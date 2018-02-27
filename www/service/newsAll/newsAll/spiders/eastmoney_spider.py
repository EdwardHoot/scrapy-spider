#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class EastmoneySpider(CrawlSpider):
    name='eastmoney'
    source = "东方财富网"
    allowed_domains = ["eastmoney.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://finance.eastmoney.com/news/ccjdd.html',
        'http://finance.eastmoney.com/news/cywjh.html',
        'http://finance.eastmoney.com/news/chgjj.html',
        'http://finance.eastmoney.com/news/cjrzb.html',
        'http://finance.eastmoney.com/news/ccyjj.html',
        'http://finance.eastmoney.com/news/cssgs.html',
        'http://finance.eastmoney.com/news/cgnjj.html',
        'http://finance.eastmoney.com/news/cgjjj.html',
        'http://finance.eastmoney.com/news/ccjxw.html',
        'http://finance.eastmoney.com/news/cjjsp.html',
        'http://finance.eastmoney.com/news/ccyts.html',
        'http://finance.eastmoney.com/news/csygc.html',
        'http://finance.eastmoney.com/news/czfgy.html',
        'http://finance.eastmoney.com/news/csyjy.html',
        'http://finance.eastmoney.com/news/cjjxr.html',
        'http://finance.eastmoney.com/news/csxy.html',
        'http://finance.eastmoney.com/news/czsdc.html',
        'http://finance.eastmoney.com/news/crdsm.html',
        'http://stock.eastmoney.com/news/cgsxw.html'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg,deny='data.eastmoney.com'),callback="parse_news",follow=True),
       # Rule(LinkExtractor(allow='_[0-9]+.html'))
        Rule(LinkExtractor(allow='_[1-6].html'))
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
        title=response.xpath('//div[@class="newsContent"]/h1/text()').extract()
        if title:
            item['title']=title
    def get_date(self,response,item):
        date=response.xpath('//div[@class="time"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'')+'00'
    def get_body(self,response,item):
        abstract=response.xpath('//div[@class="b-review"]/text()').extract()
        paras = response.xpath('//*[@id="ContentBody"]/p')
        news_body = ''
        for p in paras:
            data = p.xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    #   print entry.encode('utf-8')
                    body += line.strip()
                news_body += body + '_|_'
        item['body'] = ''.join(abstract)+'_|_'+news_body.replace('_|__|_','_|_')
