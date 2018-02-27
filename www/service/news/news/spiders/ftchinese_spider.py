#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request

class FtchineseSpider(CrawlSpider):
    name='ftchinese'
    source='FT中文网'

    def start_requests(self):
        base_urls=(
            'http://www.ftchinese.com/channel/china',
            'http://www.ftchinese.com/channel/world',
            'http://www.ftchinese.com/channel/economy',
            'http://www.ftchinese.com/channel/business'
        )

        requests = []

        for url in base_urls:
            request = Request(url, callback=self.parse_page)
            requests.append(request)

        # for url in base_urls:
        #     for i in range(2,1000):
        #         request = Request(url+'.html?page='+str(i), callback=self.parse_page)
        #         requests.append(request)

        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//div[@class="item-inner"]')
        for p in news:
            date=p.xpath('div[@class="item-time"]/text()').extract()
            if  u'1天前' in u''.join(date):
                link=''.join(p.xpath('a/@href').extract())
                yield Request('http://www.ftchinese.com'+link, callback=self.parse_news)

    def parse_news(self,response):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        self.get_source(response, item)
        self.get_title(response, item)
        self.get_date(response, item)
        self.get_body(response, item)
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
        title=response.xpath('//h1[@class="story-headline"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="story-time"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'更新于',u'').replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="story-body"]/p')
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
