#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class FunxunSpider(CrawlSpider):
    name='funxun'
    source = "房讯网"
    allowed_domains = ["funxun.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    ldate=yesterday.strftime('%Y%m%d')
    yesterday = yesterday.strftime('%Y')+yesterday.strftime('%m').replace('0','')+yesterday.strftime('%d').replace('0','')
    reg=yesterday
    start_urls = [
        'http://www.funxun.com/news/roll.asp',
        'http://www.funxun.com/news/n_more.asp?tid=34',
        'http://www.funxun.com/news/n_more.asp?tid=35',
        'http://www.funxun.com/news/n_more.asp?tid=41',
        'http://www.funxun.com/news/n_more.asp?tid=52',
        'http://www.funxun.com/news/n_more.asp?tid=53',
        'http://www.funxun.com/news/n_more.asp?tid=56',
        'http://www.funxun.com/news/n_more.asp?tid=68',
        'http://www.funxun.com/news/n_more.asp?tid=75',
        'http://www.funxun.com/news/n_more.asp?tid=76',
        'http://www.funxun.com/news/n_more.asp?tid=87',
    ]
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        Rule(LinkExtractor(allow='page=[2-3]'))
        # Rule(LinkExtractor(allow='page=[0-9]'))
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
        title=response.xpath('//div[@class="title"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="authort"]/text()').extract()
        if date:
            item['date']=self.ldate+''.join(''.join(date).replace(u':',u'').replace(u' ',u'').strip()[-6:])
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="content"]/div[1]/p')
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
