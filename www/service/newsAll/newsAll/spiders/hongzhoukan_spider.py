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

class HongzhoukanSpider(CrawlSpider):
    name='hongzhoukan'
    source='证券市场红周刊'
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')

    def start_requests(self):
        base_urls=(
            'http://news.hongzhoukan.com/article_list.php?id=394',
            'http://news.hongzhoukan.com/article_list.php?id=323',
            'http://news.hongzhoukan.com/article_list.php?id=336'
        )

        requests = []

        for url in base_urls:
            request = Request(url, callback=self.parse_page)
            requests.append(request)

        # for url in base_urls:
        #     for i in range(2,1000):
        #         request = Request(url+'&page_id='+str(i), callback=self.parse_page)
        #         requests.append(request)

        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//li')
        for p in news:
            date=p.xpath('span').extract()
            if  self.yesterday in ''.join(date):
                link=''.join(p.xpath('a/@href').extract())
                yield Request(link, callback=self.parse_news)

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
        title=response.xpath('//h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//h2/span[1]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="article"]/p')
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
