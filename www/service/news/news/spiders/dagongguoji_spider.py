#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class DaGongSpider(CrawlSpider):
    name='dagongguoji'
    source = "大公国际评级"
    allowed_domains = ["dagongcredit.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=159',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=79',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=80',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=81',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=82',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=83',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=84',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=85',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=86',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=158',
        'http://www.dagongcredit.com/index.php?m=content&c=index&a=lists&catid=87'
    ]

    # rules=(
    #     Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
    #     #Rule(LinkExtractor(allow='/index.shtml/[0-1]')),
    #     #Rule(LinkExtractor(allow='/[0-9]/dynlist.html')),
    # )
    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')
    def parse(self,response):
        yesterday = datetime.date.today()
        yesterday = yesterday.strftime('%Y%m%d')
        for i in range(19):
            item = GenericItem()
            self.get_id(response,item)
            self.get_url(response,item,i)
            self.get_source(response,item)
            self.get_title(response,item,i)
            self.get_date(response,item,i,yesterday)
            self.get_body(response,item,i)
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!remenber to Retrun Item after parse
            if item['url'] and item['date']== str(yesterday)+'000000' and item['body']:
                yield item
            else:
                continue

    def get_id(self,response,item):
        id=uuid.uuid4()
        if id:
            item['id']=id
    def get_url(self,response,item,i):
        news_url= response.xpath('//span[@class="rt"]/a/@href').extract()[i]
        if news_url:
            item['url']= ''.join(news_url).strip()
    def get_source(self,response,item):
        source=self.source
        if source:
            item['source']=source
    def get_title(self,response,item,i):
        title = response.xpath('//span[@class="rt"]/a/text()').extract()[i]
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item,i,yesterday):
        time = response.xpath('//span[@class="rt rt-time"]/text()').extract()[i]
        timebody = ''.join(time).replace(u'-',u'').strip()+'000000'
        if timebody == str(yesterday)+'000000':
            item['date']=''.join(timebody).strip()
        else:
            item['date'] = ''.join(timebody).strip()
    def get_body(self,response,item,i):
        rate = response.xpath('//span[@class="rt rt-red"]/text()').extract()[i]
        if rate:
            item['body'] = ''.join(rate).strip()