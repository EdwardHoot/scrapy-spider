#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class SouthcnSpider(CrawlSpider):
    name='southcn'
    source = "南方网"
    allowed_domains = ["southcn.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m/%d')
    reg=yesterday
    start_urls = [
        'http://economy.southcn.com/node_165826.htm',
        'http://economy.southcn.com/node_165813.htm',
        'http://economy.southcn.com/node_165834.htm',
        'http://economy.southcn.com/node_165833.htm',
        'http://economy.southcn.com/node_165839.htm',
        'http://economy.southcn.com/node_165836.htm',
        'http://economy.southcn.com/node_290151.htm',
        'http://economy.southcn.com/node_257516.htm',
        'http://economy.southcn.com/node_165838.htm',
        'http://economy.southcn.com/node_165832.htm',
        'http://economy.southcn.com/node_165812.htm',
        'http://economy.southcn.com/node_165811.htm',
        'http://finance.southcn.com/jrcj/node_188991.htm',
        'http://finance.southcn.com/f/node_123271.htm',
        'http://finance.southcn.com/cjsd/node_229651.htm',
        'http://finance.southcn.com/f/node_123279.htm',
        'http://finance.southcn.com/cfzx/node_189012.htm',
        'http://finance.southcn.com/tzrz/node_217395.htm',
        'http://finance.southcn.com/f/node_123274.htm',
        'http://finance.southcn.com/jjhq/node_189034.htm',
        'http://finance.southcn.com/ssgs/node_189041.htm',
        'http://finance.southcn.com/zqsc/node_189033.htm',
        'http://finance.southcn.com/bxzx/node_189035.htm',
        'http://finance.southcn.com/cpts/node_189037.htm',
        'http://finance.southcn.com/hygg/node_189048.htm',
        'http://finance.southcn.com/hjwh/node_189042.htm',
        'http://finance.southcn.com/qhqz/node_189045.htm',
        'http://finance.southcn.com/f/node_165971.htm',
        'http://finance.southcn.com/f/node_123273.htm',
        'http://finance.southcn.com/qyxw/node_189036.htm',
        'http://finance.southcn.com/f/node_123275.htm',
        'http://finance.southcn.com/f/node_165972.htm',
        'http://finance.southcn.com/f/node_242511.htm',
        'http://finance.southcn.com/cfzx/node_189039.htm',
        'http://finance.southcn.com/pgt/node_189032.htm',
        'http://finance.southcn.com/zhcj/node_189047.htm'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        Rule(LinkExtractor(allow='_[2-3].htm')),
        #Rule(LinkExtractor(allow='_[0-9].htm')),
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
        title=response.xpath('//*[@id="article_title"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
        if len(item['date'])<13:
            item['date']+='00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="content"]/p')
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
