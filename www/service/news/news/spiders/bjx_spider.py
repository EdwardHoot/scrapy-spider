#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class BjxSpider(CrawlSpider):
    name='bjx'
    source = "北极星电力网"
    allowed_domains = ["bjx.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://news.bjx.com.cn/list?catid=71',
        'http://news.bjx.com.cn/list?catid=89',
        'http://news.bjx.com.cn/list?catid=103',
        'http://news.bjx.com.cn/list?catid=121',
        'http://news.bjx.com.cn/list?catid=100',
        'http://news.bjx.com.cn/list?catid=111',
        'http://news.bjx.com.cn/list?catid=88',
        'http://news.bjx.com.cn/list?catid=76',
        'http://news.bjx.com.cn/list?catid=93',
        'http://news.bjx.com.cn/list?catid=85',
        'http://news.bjx.com.cn/list?catid=73',
        'http://news.bjx.com.cn/list?catid=82',
        'http://news.bjx.com.cn/list?catid=84',
        'http://news.bjx.com.cn/list?catid=110',
        'http://news.bjx.com.cn/list?catid=109',
        'http://news.bjx.com.cn/list?catid=108',
        'http://news.bjx.com.cn/list?catid=75',
        'http://news.bjx.com.cn/list?catid=79',
        'http://news.bjx.com.cn/list?catid=112',
        'http://news.bjx.com.cn/list?catid=120'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg,deny='(job)|(hr)|(-[0-9].shtml)'),callback="parse_news",follow=True),
        # Rule(LinkExtractor(allow='&page=[0-9]+'))
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
        title=response.xpath('//div[@class="hdm_left_content"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
        else:
            title = response.xpath('//div[@class="list_detail"]/h1/text()').extract()
            if title:
                item['title'] = ''.join(title).strip()
    def get_date(self,response,item):
        # date=response.xpath('//div[@class="list_copy"]/b[2]/text()').extract()
        # if date:
            item['date']=self.yesterday+"000000"
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="hdm_left_content"]/p')
        news_body = ''
        if len(paras)==0:
            paras = response.xpath('//div[@id="content"]/p')
        for p in paras:
            data = p.xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    #   print entry.encode('utf-8')
                    body += line.strip()
                news_body += body + '_|_'
        item['body'] = news_body.replace('_|__|_','_|_')
