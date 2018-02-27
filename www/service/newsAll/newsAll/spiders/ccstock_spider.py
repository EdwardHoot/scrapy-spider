#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class CcstockSpider(CrawlSpider):
    name='ccstock'
    source = "中国资本证券网"
    allowed_domains = ["ccstock.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    reg=yesterday
    start_urls = [
        'http://www.ccstock.cn/gscy/gongsi/index.html',
        'http://www.ccstock.cn/gscy/hkgongsi/index.html',
        'http://www.ccstock.cn/gscy/qiyexinxi/index.html',
        'http://www.ccstock.cn/gscy/gaoguanfangtan/index.html',
        'http://www.ccstock.cn/stock/gupiaoyaowen/index.html',
        'http://www.ccstock.cn/jrjg/bank/index.html',
        'http://www.ccstock.cn/jrjg/insurance/index.html',
        'http://www.ccstock.cn/jrjg/xintuo/index.html',
        'http://www.ccstock.cn/jrjg/quanshang/index.html',
        'http://www.ccstock.cn/finance/zcpz/index.html',
        'http://www.ccstock.cn/finance/jgzs/index.html',
        'http://www.ccstock.cn/finance/cjjs/index.html',
        'http://www.ccstock.cn/finance/people/index.html',
        'http://www.ccstock.cn/finance/sscj/index.html',
        'http://www.ccstock.cn/finance/hongguanjingji/index.html',
        'http://www.ccstock.cn/finance/hangyedongtai/index.html',
        'http://www.ccstock.cn/finance/tbbd/index.html'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
       # Rule(LinkExtractor(allow='_p[0-9]+.html'))
        Rule(LinkExtractor(allow='_p[2-3].html'))
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
        title=response.xpath('//div[@class="bt"]/h1/text()').extract()
        if title:
            item['title']=title
    def get_date(self,response,item):
        date=response.xpath('//div[@class="sub_bt"]/span/text()').extract()
        if date:
            item['date']=''.join(''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'')[-12:])+'00'
    def get_body(self,response,item):
        paras = response.xpath('//*[@id="newscontent"]/p')
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
