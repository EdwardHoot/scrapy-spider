#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class JingHuaSpider(CrawlSpider):
    name='jinghua'
    source = "京华网"
    allowed_domains = ["jinghua.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://www.jinghua.cn/',
        'http://caijing.jinghua.cn/',
        'http://caijing.jinghua.cn/zixun/',
        'http://caijing.jinghua.cn/gupiao/',
        'http://caijing.jinghua.cn/licai/',
        'http://beijing.jinghua.cn/',
        'http://news.jinghua.cn/',
        'http://tech.jinghua.cn/',
        'http://auto.jinghua.cn/',
        'http://fangchan.jinghua.cn/'
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
        title = response.xpath('//div[@class="w670"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        time = response.xpath('//div[@class="w670"]/div[@class="xinx"]/text()').extract()
        time2 = ''.join(time).strip().encode('utf-8')
        time3 = re.findall(r'\d+', str(time2)[:16] + '00')
        if time3:
            item['date']=''.join(time3).strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="article_body"]/p')
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