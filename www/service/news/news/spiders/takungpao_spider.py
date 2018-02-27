#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class TakungpaoSpider(CrawlSpider):
    name='takungpao'
    source = "大公报"
    allowed_domains = ["takungpao.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y/%m%d')
    reg=yesterday
    start_urls = [
        'http://finance.takungpao.com/financial/jrtx/',
        'http://finance.takungpao.com/financial/yzcp/',
        'http://finance.takungpao.com/financial/tfnc/',
        'http://finance.takungpao.com/financial/ssgs/',
        'http://finance.takungpao.com/financial/gnzz/',
        'http://finance.takungpao.com/hkstock/cjss/',
        'http://finance.takungpao.com/hkstock/gsyw/',
        'http://finance.takungpao.com/hkstock/jgsd/',
        'http://finance.takungpao.com/hkstock/qqgs/',
        'http://finance.takungpao.com/hkstock/gjjj/',
        'http://finance.takungpao.com/hkstock/jjyz/',
        'http://finance.takungpao.com/gscy/yaowen/',
        'http://finance.takungpao.com/gscy/gsxw/',
        'http://finance.takungpao.com/gscy/shxf/',
        'http://finance.takungpao.com/gscy/msyq/',
        'http://finance.takungpao.com/gscy/sxy/',
        'http://finance.takungpao.com/tech/appliance/',
        'http://finance.takungpao.com/tech/focus/',
        'http://finance.takungpao.com/tech/internet/',
        'http://finance.takungpao.com/tech/it/',
        'http://finance.takungpao.com/tech/mobile/',
        'http://finance.takungpao.com/tech/new-media/',
        'http://finance.takungpao.com/tech/zggng/',
        'http://finance.takungpao.com/tech/kjzl/',
        'http://finance.takungpao.com/tech/topic/',
        'http://finance.takungpao.com/tech/explore/',
        'http://finance.takungpao.com/tech/kjgd/',
        'http://food.takungpao.com/roll',
        'http://food.takungpao.com/opinion',
        'http://food.takungpao.com/complaint',
        'http://food.takungpao.com/industry/trend',
        'http://food.takungpao.com/expense',
        'http://food.takungpao.com/authority',
        'http://food.takungpao.com/topic',
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
        title=response.xpath('//h1[@class="tpk_con_tle"]/text()').extract()
        if title:
            item['title']=title
    def get_date(self,response,item):
        date=response.xpath('//div[@class="fl_dib"]/text()').extract()[0]
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="tpk_text clearfix"]/p')
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
