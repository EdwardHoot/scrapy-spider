#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class StockTimesSpider(CrawlSpider):
    name='stocktimes'
    source = "证券时报"
    allowed_domains = ["stcn.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y/%m%d')
    reg=yesterday
    start_urls = [
        'http://www.stcn.com/',
        'http://kuaixun.stcn.com/index.shtml',
        'http://kuaixun.stcn.com/index_2.shtml',
        'http://kuaixun.stcn.com/index_3.shtml',
        'http://kuaixun.stcn.com/index_4.shtml',
        'http://kuaixun.stcn.com/index_5.shtml',
        'http://kuaixun.stcn.com/index_6.shtml',
        'http://kuaixun.stcn.com/index_7.shtml',
        'http://kuaixun.stcn.com/index_8.shtml',
        'http://kuaixun.stcn.com/index_9.shtml',
        'http://kuaixun.stcn.com/index_10.shtml',
        'http://kuaixun.stcn.com/index_11.shtml',
        'http://kuaixun.stcn.com/index_12.shtml',
        'http://kuaixun.stcn.com/index_13.shtml',
        'http://kuaixun.stcn.com/index_14.shtml',
        'http://kuaixun.stcn.com/index_15.shtml',
        'http://kuaixun.stcn.com/index_16.shtml',
        'http://kuaixun.stcn.com/index_17.shtml',
        'http://kuaixun.stcn.com/index_18.shtml',
        'http://kuaixun.stcn.com/index_19.shtml',
        'http://kuaixun.stcn.com/index_20.shtml',
        'http://stock.stcn.com/dapan/index.shtml',
        'http://stock.stcn.com/bankuai/index.shtml',
        'http://stock.stcn.com/zhuli/index.shtml',
        'http://kuaixun.stcn.com/list/kxyb.shtml',
        'http://stock.stcn.com/xingu/index.shtml',
        'http://company.stcn.com/gsxw/index.shtml',
        'http://company.stcn.com/cjnews/index.shtml',
        'http://company.stcn.com/cjnews/index.shtml',
        'http://finance.stcn.com/quanshang/index.shtml',
        'http://finance.stcn.com/yxlc/index.shtml',
        'http://finance.stcn.com/baoxian/index.shtml',
        'http://finance.stcn.com/xintuo/index.shtml',
        'http://finance.stcn.com/qihuo/index.shtml',
        'http://data.stcn.com/',
        'http://sanban.stcn.com/gsyyb/index.shtml',
        'http://sanban.stcn.com/zcysc/index.shtml'
    ]

    rules=(
        Rule(LinkExtractor(allow=reg),callback="parse_news",follow=True),
        #Rule(LinkExtractor(allow='/index.shtml/[0-1]')),
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
        title = response.xpath('//div[@class="intal_tit"]/h2/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        time = response.xpath('//div[@class="intal_tit"]/div[@class="info"]/text()').extract()
        time2 = ''.join(time).strip().encode('utf-8')
        time3 = re.findall(r'\d+', str(time2) + '00')
        if time3:
            item['date']=''.join(time3).strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="txt_con"]/p')
        news_body = ''
        for p in paras:
            data = p.xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    body += line.strip()
                news_body += body + '_|_'
        if news_body:
            item['body'] = ''.join(news_body).replace('_|__|_','_|_').strip()