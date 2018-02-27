#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class SohuSpider(CrawlSpider):
    name='sohu'
    source = "搜狐财经"
    allowed_domains = ["sohu.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://business.sohu.com/hgjj/',
        'http://business.sohu.com/qyjj',
        'http://business.sohu.com/xflc',
        'http://business.sohu.com/cht',
        'http://business.sohu.com/gskb',
        'http://business.sohu.com/gsbg',
        'http://business.sohu.com/gscx',
        'http://business.sohu.com/gsfz',
        'http://business.sohu.com/s2011/ipo',
        'http://business.sohu.com/s2011/shangshigongsi',
        'http://business.sohu.com/sdwz',
        'http://business.sohu.com/investigator',
        'http://business.sohu.com/nengyuan',
        'http://business.sohu.com/industry',
        'http://business.sohu.com/qiche',
        'http://business.sohu.com/fangdichan',
        'http://business.sohu.com/keji',
        'http://business.sohu.com/lingshou',
        'http://business.sohu.com/jrjg',
        'http://business.sohu.com/jqgg',
        'http://business.sohu.com/simu',
        'http://business.sohu.com/c241863626',
        'http://business.sohu.com/jrqj',
        'http://business.sohu.com/s2004/2066/s222393258.shtml',
        'http://business.sohu.com/s2004/2066/s222393246.shtml',
        'http://business.sohu.com/s2008/2066/s259192864',
        'http://business.sohu.com/s2004/2066/s222393324.shtml',
        'http://business.sohu.com/s2006/2066/s241844915',
        'http://business.sohu.com/s2004/2066/s222393277.shtml',
        'http://business.sohu.com/s2004/2066/s222393386.shtml',
        'http://business.sohu.com/quanqiu',
        'http://business.sohu.com/shangpin',
        'http://business.sohu.com/zgysj'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg,deny='tv.sohu.com'),callback="parse_news",follow=True),
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
        title=response.xpath('//div[@class="content-box clear"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//*[@id="pubtime_baidu"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        paras=response.xpath('//div[@id="contentText"]/p')
        if not paras:
            paras = response.xpath('//div[@id="contentText"]/div[1]/p')
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
