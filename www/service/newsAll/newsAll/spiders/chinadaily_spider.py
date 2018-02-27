#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class ChinadailySpider(CrawlSpider):
    name='chinadaily'
    source = "中国日报中文网"
    allowed_domains = ["caijing.chinadaily.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m/%d')
    reg=yesterday
    start_urls = [
        'http://caijing.chinadaily.com.cn/node_1078506.htm',
        'http://caijing.chinadaily.com.cn/node_1119881.htm',
        'http://caijing.chinadaily.com.cn/node_1078505.htm',
        'http://caijing.chinadaily.com.cn/node_1078507.htm',
        'http://caijing.chinadaily.com.cn/node_1078504.htm',
        'http://caijing.chinadaily.com.cn/node_1078513.htm',
        'http://caijing.chinadaily.com.cn/node_1078508.htm',
        'http://caijing.chinadaily.com.cn/node_1078503.htm',
        'http://caijing.chinadaily.com.cn/node_1078515.htm',
        'http://caijing.chinadaily.com.cn/node_1119905.htm',
        'http://caijing.chinadaily.com.cn/node_1119884.htm',
    ]
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        Rule(LinkExtractor(allow='_[2-4].htm'))
        # Rule(LinkExtractor(allow='/_[0-9].htm'))
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
        title=response.xpath('//h1[@class="dabiaoti"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//*[@id="pubtime"]/text()').extract()[0]
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="Content"]/p')
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
