#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class CsSpider(CrawlSpider):
    name='cs'
    source = "中证网"
    allowed_domains = ["cs.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://www.cs.com.cn/xwzx/hg/',
        'http://www.cs.com.cn/xwzx/jr/',
        'http://www.cs.com.cn/xwzx/cj/',
        'http://www.cs.com.cn/xwzx/ms/',
        'http://www.cs.com.cn/hw/hwgsbd/',
        'http://www.cs.com.cn/hw/03/',
        'http://www.cs.com.cn/hw/hqzx/',
        'http://www.cs.com.cn/gg/gsxw/',
        'http://www.cs.com.cn/ssgs/gsxw/',
        'http://www.cs.com.cn/ssgs/gssd/',
        'http://www.cs.com.cn/ssgs/hyzx/',
        'http://www.cs.com.cn/ssgs/fcgs/',
        'http://www.cs.com.cn/ssgs/qcgs/',
        'http://www.cs.com.cn/ssgs/bxgs/',
        'http://www.cs.com.cn/ssgs/gsnjd/',
        'http://www.cs.com.cn/xwzx/gsyq/'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg), callback="parse_news", follow=True),
        Rule(LinkExtractor(allow='_[1-3].html')),
        # Rule(LinkExtractor(allow='_[0-9].html')),
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
        title=response.xpath('//h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="Ff"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="artical_c"]/p')
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
