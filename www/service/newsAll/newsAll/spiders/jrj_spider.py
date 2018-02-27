#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class JrjSpider(CrawlSpider):
    name='jrj'
    source = "金融界"
    allowed_domains = ["jrj.com.cn","jrj.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y/%m/%d')
    reg=yesterday
    print reg
    start_urls = [
        'http://stock.jrj.com/list/stockssgs.shtml',
        'http://stock.jrj.com.cn/list/stockgszx.shtml',
        'http://stock.jrj.com.cn/hotstock/gnjj.shtml'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg), callback="parse_news", follow=True),
        Rule(LinkExtractor(allow='-[2-6].shtml')),
        # Rule(LinkExtractor(allow='-[0-9].shtml')),
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
        title=response.xpath('//div[@class="titmain"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//p[@class="inftop"]/span[1]/text()').extract()
        if not date:
            date=response.xpath('//p[@class="time"][1]/text()').extract()
        if not date:
            date = response.xpath('//span[@class="time"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="texttit_m1"]/p')
        news_body = ''
        for p in paras:
            data = p.xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    #   print entry.encode('utf-8')
                    body += line.strip()
                news_body += body + '_|_'
        if news_body.find(u'人人有份儿'):
            news_body=''.join(news_body[news_body.index(u'人人有份儿')+5:])
        item['body'] = news_body.replace('_|__|_','_|_')
