#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class BeiJiaoSpider(CrawlSpider):
    name='beijiaosuo'
    source = "北京产权交易所"
    allowed_domains = ["cbex.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    lastmonth = yesterday.strftime('%Y%m')
    reg=lastmonth
    yesterday = yesterday.strftime('%Y%m%d')
    start_urls = [
        'http://www.cbex.com.cn/',
        'http://www.cbex.com.cn/article/ggyts/lsgg/',
        'http://www.cbex.com.cn/article/xxpd/bjsdt/',
        'http://www.cbex.com.cn/article/xxpd/yjdt/',
        'http://www.cbex.com.cn/article/xxpd/bjssj/',
        'http://www.cbex.com.cn/article/xxpd/mtbd/',
        'http://www.cbex.com.cn/article/zcfg/zhfg/'
    ]

    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        Rule(LinkExtractor(allow='/index.shtml/[0-1]')),
        #Rule(LinkExtractor(allow='/[0-9]/dynlist.html')),
    )
    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')
    def parse_news(self,response):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        reday = yesterday.strftime('%d')
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        self.get_source(response,item)
        self.get_title(response,item)
        self.get_date(response,item)
        self.get_body(response,item)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!remenber to Retrun Item after parse
        if item['body'] and item['date'][6:8] == reday:
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
        title = response.xpath('//div[@class="text"]/h3/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        time = response.xpath('//script[@type="text/javascript"]/text()').extract()
        time2 = ''.join(time).strip()
        time3 = re.findall(r'var tm = ".*";', time2)
        time4 = re.findall(r'\d+', str(time3) + '00')
        if time4:
            item['date']=''.join(time4).strip()
    def get_body(self,response,item):
        paras = response.xpath('//table[@class="aarticle"]/tr/td/text()').extract()
        paraas = response.xpath('//table[@class="aarticle"]/tr/td/p')

        news_body = ''
        for p in paraas:
            data = p.xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    body += line.strip()
                news_body += body + '_|_'

        contentbody1 = ''.join(paras).strip()
        contentbody2 = ''.join(news_body).replace('_|__|__|__|_', '_|_').replace('_|__|__|_', '_|_').replace('_|__|_','_|_').strip()
        contentbody = contentbody1+contentbody2
        if contentbody:
            item['body'] = contentbody