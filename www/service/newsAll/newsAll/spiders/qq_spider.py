#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class QqSpider(CrawlSpider):
    name='qq'
    source = "腾讯财经"
    allowed_domains = ["qq.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    base_urls = [
        'http://finance.qq.com/c/gsbdlist_***.htm',
        'http://finance.qq.com/c/hgjjllist_***.htm',
        'http://finance.qq.com/c/jrscllist_***.htm',
    ]
    start_urls = []
    for url in base_urls:
        for i in range(8):
            start_urls.append(url.replace('***',str(i)))

    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
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
        title=response.xpath('//h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="a_time"]/text()').extract()
        if not date:
            date = response.xpath('//span[@class="pubTime article-time"]/text()').extract()
        if not date:
            date = response.xpath('//span[@class="a_time"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="Cnt-Main-Article-QQ"]/p')
        news_body = ''
        for p in paras:
            data = p.xpath('text()').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    #   print entry.encode('utf-8')
                    body += line.strip().replace(' ','')
                news_body += body + '_|_'
        item['body'] = news_body.replace('_|__|_','_|_')
