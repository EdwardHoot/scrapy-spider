#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class NbdSpider(CrawlSpider):
    name='gmw'
    source = "光明网"
    allowed_domains = ["gmw.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m/%d')
    reg=yesterday
    start_urls = [
        'http://news.gmw.cn/node_23545.htm',
        'http://economy.gmw.cn/node_8971.htm',
        'http://economy.gmw.cn/node_8994.htm',
        'http://economy.gmw.cn/node_8987.htm',
        'http://economy.gmw.cn/node_8976.htm',
        'http://economy.gmw.cn/node_12468.htm',
        'http://economy.gmw.cn/node_8992.htm',
        'http://economy.gmw.cn/node_8999.htm',
        'http://economy.gmw.cn/node_8990.htm',
        'http://economy.gmw.cn/node_12497.htm',
        'http://economy.gmw.cn/node_12466.htm',
        'http://economy.gmw.cn/node_12467.htm',
        'http://economy.gmw.cn/node_8996.htm',
        'http://economy.gmw.cn/node_33512.htm',
        'http://economy.gmw.cn/node_12751.htm',
        'http://economy.gmw.cn/node_12750.htm',
        'http://economy.gmw.cn/node_12749.htm',
        'http://economy.gmw.cn/node_12801.htm',
        'http://economy.gmw.cn/node_12802.htm',
        'http://economy.gmw.cn/node_12803.htm',
        'http://economy.gmw.cn/node_12804.htm',
        'http://economy.gmw.cn/node_12748.htm',
        'http://shipin.gmw.cn/node_35759.htm',
        'http://www.gmw.cn/ny/node_22814.htm',
        'http://it.gmw.cn/node_29402.htm',
        'http://it.gmw.cn/node_4487.htm',
        'http://finance.gmw.cn/node_42534.htm',
        'http://finance.gmw.cn/node_42544.htm',
        'http://finance.gmw.cn/node_42671.htm',
        'http://finance.gmw.cn/node_42547.htm'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg,deny='(photo)|(epaper)|(life)'),callback="parse_news",follow=True),
        #Rule(LinkExtractor(allow='_[0-9].html',deny='(photo)|(epaper)')),
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
        title=response.xpath('//*[@id="articleTitle"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//*[@id="pubTime"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
    def get_body(self,response,item):
        paras = response.xpath('//*[@id="contentMain"]/p')
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
