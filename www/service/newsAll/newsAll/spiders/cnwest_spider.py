#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class CnwestSpider(CrawlSpider):
    name='cnwest'
    source = "陕西新闻网"
    allowed_domains = ["cnwest.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m/%d')
    reg=yesterday
    start_urls = [
        'http://finance.cnwest.com/node_13545.htm',
        'http://finance.cnwest.com/node_13575.htm',
        'http://finance.cnwest.com/node_13570.htm'
    ]
    rules=(
        Rule(LinkExtractor(allow='http://finance.cnwest.com/content/'+reg),callback="parse_news",follow=True),
        Rule(LinkExtractor(allow='node_._[2-3].html'))
        # Rule(LinkExtractor(allow='node_._[0-9].html'))
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
        title=response.xpath('//div[@class="headnav"]/div[@class="layout"][2]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@class="layout timely"]/div[@class="layout-left"]/p/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'时间：',u'').replace(u'-',u'').replace(u':',u'').replace(u' ',u'').replace(u'"',u'').strip()[:14]
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="con-detail"]/p')
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
