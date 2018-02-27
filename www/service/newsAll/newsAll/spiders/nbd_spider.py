#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class NbdSpider(CrawlSpider):
    name='nbd'
    source = "每经网"
    allowed_domains = ["nbd.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    reg=yesterday
    start_urls = [
        'http://www.nbd.com.cn/columns/395',
        'http://www.nbd.com.cn/columns/394',
        'http://www.nbd.com.cn/columns/392',
        'http://www.nbd.com.cn/columns/255',
        'http://www.nbd.com.cn/columns/140',
        'http://www.nbd.com.cn/columns/223',
        'http://www.nbd.com.cn/columns/130',
        'http://www.nbd.com.cn/columns/396',
        'http://www.nbd.com.cn/columns/397',
        'http://www.nbd.com.cn/columns/398',
        'http://www.nbd.com.cn/columns/399',
        'http://www.nbd.com.cn/columns/400',
        'http://www.nbd.com.cn/columns/26',
        'http://www.nbd.com.cn/columns/24',
        'http://www.nbd.com.cn/columns/3',
        'http://www.nbd.com.cn/columns/2',
        'http://economy.nbd.com.cn/columns/311',
        'http://economy.nbd.com.cn/columns/44',
        'http://economy.nbd.com.cn/columns/313',
        'http://economy.nbd.com.cn/columns/315',
        'http://economy.nbd.com.cn/columns/316',
        'http://stocks.nbd.com.cn/columns/319',
        'http://stocks.nbd.com.cn/columns/318',
        'http://stocks.nbd.com.cn/columns/275',
        'http://stocks.nbd.com.cn/columns/12',
        'http://stocks.nbd.com.cn/columns/28',
        'http://stocks.nbd.com.cn/columns/405',
        'http://stocks.nbd.com.cn/columns/403',
        'http://industry.nbd.com.cn/columns/340',
        'http://industry.nbd.com.cn/columns/39',
        'http://industry.nbd.com.cn/columns/45',
        'http://industry.nbd.com.cn/columns/341',
        'http://industry.nbd.com.cn/columns/256',
        'http://industry.nbd.com.cn/columns/342',
        'http://industry.nbd.com.cn/columns/343',
        'http://industry.nbd.com.cn/columns/344',
        'http://industry.nbd.com.cn/columns/345',
        'http://industry.nbd.com.cn/columns/346',
        'http://finance.nbd.com.cn/columns/120',
        'http://finance.nbd.com.cn/columns/415',
        'http://finance.nbd.com.cn/columns/314',
        'http://finance.nbd.com.cn/columns/326',
        'http://finance.nbd.com.cn/columns/26',
        'http://finance.nbd.com.cn/columns/122',
        'http://finance.nbd.com.cn/columns/123',
        'http://finance.nbd.com.cn/columns/327',
        'http://finance.nbd.com.cn/columns/328',
        'http://finance.nbd.com.cn/columns/329'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg,deny='m.nbd.com.cn'),callback="parse_news",follow=True),
        #Rule(LinkExtractor(allow='/page/[0-9]')),
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
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="time"]/text()').extract()
        if not date:
            date = response.xpath('//p[@class="article-messge"]/span[1]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="g-articl-text"]/p')
        if not paras:
            paras = response.xpath('//div[@class="main-left-article"]/p')
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
