#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class SinaSpider(CrawlSpider):
    name='sina'
    source = "新浪财经"
    allowed_domains = ["sina.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    reg=yesterday
    start_urls = [
        'http://roll.finance.sina.com.cn/finance/cj4/cj_gsxw/index.shtml',
        'http://roll.finance.sina.com.cn/finance/cj4/cj_cyxw/index.shtml',
        'http://roll.finance.sina.com.cn/finance/cj4/rsbd/index.shtml',
        'http://roll.finance.sina.com.cn/finance/cj4/sdbd/index.shtml',
        'http://roll.finance.sina.com.cn/finance/cj4/jcgc/index.shtml',
        'http://roll.finance.sina.com.cn/finance/cj4/zsscdt/index.shtml'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        Rule(LinkExtractor(allow='index_[2-3]+.shtml'))
        #Rule(LinkExtractor(allow='index_[0-9]+.shtml'))
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
        title=response.xpath('//*[@id="artibodyTitle"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="time-source"]/text()').extract()
        if not date:
            date=response.xpath('//span[@id="pub_date"]/text()').extract()
        if date[0]:
            date=date[0]
        if date:
            item['date']=''.join(''.join(date).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').replace(u'"',u'').strip()[:12])+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="artibody"]/p')
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
