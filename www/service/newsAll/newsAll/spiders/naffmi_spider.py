#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
class NaffmiSpider(CrawlSpider):
    name='naffmi'
    source = "中国银行间市场交易商协会"
    allowed_domains = ["nafmii.org.cn"]
    month = datetime.date.today() - datetime.timedelta(days=1)
    month = month.strftime('%Y%m%d')
    reg = month + '*'
    start_urls = ['http://www.nafmii.org.cn/dcmfx/tzs/scp/',
                  'http://www.nafmii.org.cn/dcmfx/tzs/smecn/',
                  'http://www.nafmii.org.cn/dcmfx/tzs/cp/',
                  'http://www.nafmii.org.cn/dcmfx/tzs/mtn/',
                  'http://www.nafmii.org.cn/dcmfx/tzs/ppn/',
                  'http://www.nafmii.org.cn/dcmfx/tzs/zczcpj/',
                  'http://www.nafmii.org.cn/dcmfx/tzs/PRN1/',
                  'http://www.nafmii.org.cn/dcmfx/tzs/zced/',
                  'http://www.nafmii.org.cn/dcmfx/tzs/dfi/',
                  'http://www.nafmii.org.cn/dcmfx/tzs/gn/']
    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        # Rule(LinkExtractor(allow='_[0-9]+.html'))
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
        title=response.xpath('//div[@class="Section1"]/p[10]/span[1]/text()').extract()
        if title:
            item['title']=(''.join(title)+u'接受注册通知书').replace(u"：",u"").replace(u" ",u"")
    def get_date(self,response,item):
        date=response.url[-19:-11]
        item['date']=date+u'000000'

    def get_body(self,response,item):
        paras = response.xpath('//div[@class="Section1"]/p')
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


