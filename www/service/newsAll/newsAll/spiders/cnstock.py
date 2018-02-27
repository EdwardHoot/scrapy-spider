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

class CnstockSpider(CrawlSpider):
    name='cnstock'
    source = "中国证券网"
    allowed_domains = ["cnstock.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%m%d')

    def start_requests(self):
        base_urls=(
            'http://caifu.cnstock.com/list/jj_shidian/',
            'http://caifu.cnstock.com/list/jj_chanping_jvjiao/',
            'http://caifu.cnstock.com/list/jj_gongsi_jvjiao/',
            'http://caifu.cnstock.com/list/jj_yenei_dongtai/',
            'http://caifu.cnstock.com/list/yh_yinghang_yaowen/',
            'http://caifu.cnstock.com/list/xt_gongsi_jvjiao/',
            'http://caifu.cnstock.com/list/bonds/',
            'http://caifu.cnstock.com/list/sm_dongtai/',
            'http://company.cnstock.com/lists/gszx/',
            'http://company.cnstock.com/gszj/gsdy/',
            'http://company.cnstock.com/gszj/rdgs/',
            'http://news.cnstock.com/news/sns_zxk/',
            'http://news.cnstock.com/news/sns_yw/',
            'http://yjbg.cnstock.com/gsjz/',
            'http://ggjd.cnstock.com/gglist/search/hyzs/',
            'http://ggjd.cnstock.com/gglist/search/jdhc/',
            'http://ggjd.cnstock.com/gglist/search/qmtbbdj/',
            'http://ggjd.cnstock.com/gglist/search/ggkx/',
            'http://irm.cnstock.com/ivlist/index/yqjj/',
        )
        requests = []

        for url in base_urls:
            request = Request(url, callback=self.parse_page)
            requests.append(request)

        for url in base_urls:
            for i in range(2,3):
                request = Request(url+ str(i), callback=self.parse_page)
                requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//li')
        for p in news:
            date=''.join(p.xpath('span[@class="time"]/text()').extract()).replace(u'/',u'').replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
            if date and self.yesterday in date:
                link=''.join(p.xpath('a/@href').extract())
                yield Request(link, callback=self.parse_news)

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
        title=response.xpath('//h1[@class="title"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="timer"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="qmt_content_div"]/p')

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
