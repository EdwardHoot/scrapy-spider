#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class XiaoXiangSpider(CrawlSpider):
    name='xiaoxiangcb'
    source = "潇湘晨报网"
    allowed_domains = ["stcn.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    reg=yesterday
    start_urls = [
        'http://www.xxcb.cn/caijing/',
        'http://www.xxcb.cn/caijing/yh/',
        'http://www.xxcb.cn/caijing/bx/',
        'http://www.xxcb.cn/caijing/zq/',
        'http://www.xxcb.cn/event/',
        'http://www.xxcb.cn/house/'
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
        title = response.xpath('//div[@class="at_content_main"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        time = response.xpath('//span[@id="pubtime_baidu"]/span[@id="comment-time"]/text()').extract()
        time2 = ''.join(time).strip().encode('utf-8')
        time3 = re.findall(r'\d+', str(time2))
        if time3:
            item['date']=''.join(time3).strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="endPc"]/div[@style="float: left"]/p')
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