#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request

class ZjSpider(CrawlSpider):
    name='zj'
    source='浙江新闻网'

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y/%m/%d')
    def start_requests(self):
        base_urls=(
            'http://news.zj.com/list/13/',
            'http://news.zj.com/list/15/',
            'http://news.zj.com/list/22/',
            'http://news.zj.com/list/36/',
            'http://news.zj.com/list/37/',
            'http://news.zj.com/list/38/'
        )

        requests = []

        for url in base_urls:
            for i in range(1,2):
                request = Request(url+str(i)+'.html', callback=self.parse_page)
                requests.append(request)

        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//li')
        for p in news:
            link = ''.join(p.xpath('span[1]/a/@href').extract())
            if  self.yesterday in ''.join(link):
                if link.startswith('http'):
                    yield Request(link, callback=self.parse_news)
                else:
                    yield Request('http://news.zj.com'+link, callback=self.parse_news)

    def parse_news(self,response):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        self.get_source(response, item)
        self.get_title(response, item)
        self.get_date(response, item)
        self.get_body(response, item)
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
        title=response.xpath('//div[@class="adetail_bt lz"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@class="adetail_time"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'发布日期：',u'').replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="adetail_wz awz_zhong"]/p')
        if not paras:
            paras = response.xpath('//div[@class="adetail_wz awz_zhong"]/div')
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
