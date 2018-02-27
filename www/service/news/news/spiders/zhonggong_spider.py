#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class ZhongGongSpider(CrawlSpider):
    name='zhonggong'
    source = "中工网"
    allowed_domains = ["workercn.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m/%d')
    reg=yesterday
    start_urls = [
        'http://finance.workercn.cn/',
        'http://finance.workercn.cn/526/526.shtml',
        'http://finance.workercn.cn/527/527.shtml',
        'http://finance.workercn.cn/528/528.shtml',
        'http://finance.workercn.cn/529/529.shtml',
        'http://finance.workercn.cn/530/530.shtml',
        'http://finance.workercn.cn/531/531.shtml',
        'http://finance.workercn.cn/532/532.shtml',
        'http://finance.workercn.cn/533/533.shtml',
        'http://finance.workercn.cn/534/534.shtml',
        'http://finance.workercn.cn/535/535.shtml',
        'http://finance.workercn.cn/536/536.shtml',
        'http://finance.workercn.cn/537/537.shtml',
        'http://firm.workercn.cn/',
        'http://firm.workercn.cn/495/495.shtml',
        'http://firm.workercn.cn/496/496.shtml',
        'http://firm.workercn.cn/497/497.shtml',
        'http://firm.workercn.cn/498/498.shtml',
        'http://firm.workercn.cn/499/499.shtml',
        'http://firm.workercn.cn/500/500.shtml',
        'http://firm.workercn.cn/792/792.shtml',
        'http://firm.workercn.cn/502/502.shtml',
        'http://firm.workercn.cn/503/503.shtml',
        'http://firm.workercn.cn/504/504.shtml',
        'http://firm.workercn.cn/505/505.shtml',
        'http://acftu.workercn.cn/',
        'http://acftu.workercn.cn/27/27.shtml'
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
        title = response.xpath('//div[@style="width:92%; height:auto; text-align:center; padding-top:10px; margin:0 auto;"]/span/b/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        time = response.xpath('//div[@class="ad_main"]/span[@class="ad_tl_time"]/text()').extract()
        time2 = ''.join(time).strip().encode('utf-8')
        time3 = re.findall(r'\d+', str(time2))
        time4 = ''.join(time3).strip()+'000000'
        if time4:
            item['date']= time4[:14]
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="ad_content"]/p')
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