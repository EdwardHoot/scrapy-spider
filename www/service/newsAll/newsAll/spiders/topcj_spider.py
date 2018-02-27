#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class TopcjSpider(CrawlSpider):
    name='topcj'
    source = "顶点财经"
    allowed_domains = ["topcj.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://www.topcj.com/html/100/DDYC/',
        'http://www.topcj.com/html/2/WEB_JRTT/',
        'http://www.topcj.com/html/2/YDDP/',
        'http://www.topcj.com/html/5/BKFY/',
        'http://www.topcj.com/html/1/CJXW/',
        'http://www.topcj.com/html/7/HQSM/',
        'http://www.topcj.com/html/3/CYZX/',
        'http://www.topcj.com/html/7/SCZM/',
        'http://www.topcj.com/html/4/SCCL/',
        'http://www.topcj.com/html/4/SCGC/',
        'http://www.topcj.com/html/4/ZLDX/',
        'http://www.topcj.com/html/4/MRTJ/',
        'http://www.topcj.com/html/1/GGYW/',
        'http://www.topcj.com/html/6/AHZT/',
        'http://www.topcj.com/html/1/ZHZX/'
        'http://www.topcj.com/html/2/QZ1/',
        'http://www.topcj.com/html/3/ZXBYW/',
        'http://www.topcj.com/html/3/HYYJ/',
        'http://www.topcj.com/html/2/KHGG/',
        'http://www.topcj.com/html/2/KPGG/',
        'http://www.topcj.com/html/2/KKGG/',
        'http://www.topcj.com/html/0/GSGG/',
        'http://www.topcj.com/html/0/GSXW/',
        'http://www.topcj.com/html/0/GSBD/',
        'http://www.topcj.com/html/2/SJDP/',
        'http://www.topcj.com/html/1/JJXW/',
        'http://www.topcj.com/html/6/JJYJ/',
        'http://www.topcj.com/html/2/JJRY/',
        'http://www.topcj.com/html/2/XGYW/',
        'http://www.topcj.com/html/2/XGDJ/',
        'http://www.topcj.com/html/1/CYB/'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        # Rule(LinkExtractor(allow='_[0-9]+.shtml'))
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
        title=response.xpath('//div[@class="articleCenter"]/h2/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@class="articleTitle"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'"',u'').replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u'来源',u'').replace(u'出处',u'').replace(u' ',u'')
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="art"]/p')
        news_body = ''
        if len(paras) == 0:
            data = response.xpath('//div[@id="art"]').xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    #   print entry.encode('utf-8')
                    body += line.strip()
                news_body += body + '_|_'
        for p in paras:
            data = p.xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    #   print entry.encode('utf-8')
                    body += line.strip()
                news_body += body + '_|_'
        item['body'] = news_body.replace('_|__|_','_|_')
