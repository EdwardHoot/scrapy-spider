#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class IfengSpider(CrawlSpider):
    name='ifeng'
    source = "凤凰财经"
    allowed_domains = ["ifeng.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://finance.ifeng.com/cmppdyn/756/665/1/dynlist.html',
        'http://finance.ifeng.com/cmppdyn/771/843/1/dynlist.html',
        'http://finance.ifeng.com/cmppdyn/759/611/1/dynlist.html',
        'http://finance.ifeng.com/cmppdyn/26/33/1/dynlist.html'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg,deny='ent.'),callback="parse_news",follow=True),
        Rule(LinkExtractor(allow='/[2-3]/dynlist.html')),
        #Rule(LinkExtractor(allow='/[0-9]/dynlist.html')),
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
        title=response.xpath('//*[@id="artical_topic"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="ss01"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="main_content"]/p')
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
