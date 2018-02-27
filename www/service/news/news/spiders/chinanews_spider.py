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

class ChinanewsSpider(CrawlSpider):
    name='chinanews'
    source = "中国新闻网"
    allowed_domains = ["chinanews.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y/%m-%d')

    def start_requests(self):
        requests = []
        base_urls = [
            'http://channel.chinanews.com/cns/cl/cj-hgds.shtml',
            'http://channel.chinanews.com/cns/cl/cj-chjxw.shtml',
            'http://channel.chinanews.com/cns/cl/cj-sczx.shtml',
            'http://channel.chinanews.com/cns/u/finance/gs.shtml',
            'http://channel.chinanews.com/cns/cl/cj-gjcj.shtml',
            'http://channel.chinanews.com/cns/cl/cj-fyrw.shtml',
            'http://channel.chinanews.com/u/jryj.shtml',
            'http://channel.chinanews.com/u/jrhg.shtml',
            'http://channel.chinanews.com/cns/cl/fortune-jgdtyh.shtml',
            'http://channel.chinanews.com/u/stock/sh.shtml',
            'http://channel.chinanews.com/cns/cl/stock-jgzc.shtml',
            'http://channel.chinanews.com/cns/cl/stock-gsxw.shtml',
            'http://channel.chinanews.com/u/estate/estate-zdgz.shtml',
            'http://channel.chinanews.com/cns/cl/estate-hb.shtml',
            'http://channel.chinanews.com/u/ny/hy.shtml',
            'http://channel.chinanews.com/u/ny/qy.shtml',
            'http://channel.chinanews.com/u/ny/jn.shtml',
            'http://channel.chinanews.com/cns/cl/ny-nyxy.shtml',
            'http://channel.chinanews.com/cns/cl/ny-xny.shtml',
            'http://channel.chinanews.com/cns/cl/ny-hqsc.shtml',
            'http://channel.chinanews.com/cns/cl/wine-yw.shtml',
            'http://channel.chinanews.com/cns/cl/wine-hy.shtml',
            'http://channel.chinanews.com/cns/cl/wine-sc.shtml'
        ]
        for url in base_urls:
            requests.append(Request(url, callback=self.parse_page))
            # for i in range(1,360):
            #     requests.append(Request(url+'?pager='+str(i),callback=self.parse_page))
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self, response):
        news = response.xpath('//td')
        for p in news:
            url=''.join(p.xpath('a/@href').extract()).strip()
            if url and self.yesterday in url:
                yield Request(url,callback=self.parse_news)

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
        title=response.xpath('//div[@id="cont_1_1_2"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@class="left-t"]/text()').extract()[0]
        if date:
            item['date']=''.join(''.join(date).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()[:12])+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="left_zw"]/p')
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
