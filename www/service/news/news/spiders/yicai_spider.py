#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request

class YicaiSpider(CrawlSpider):
    name='yicai'
    source='第一财经'
    allowed_domains = ["yicai.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')

    def start_requests(self):
        keywords=(
            '/90',
            '/91',
            '/95',
            '/97',
            '/203',
            '/92',
            '/93'
        )
        requests = []
        base_urls = [
            'http://www.yicai.com/news/finance/',
            'http://www.yicai.com/news/markets/',
            'http://www.yicai.com/news/business/',
            'http://www.yicai.com/news/consumer/',
            'http://www.yicai.com/news/opinion/',
            'http://www.yicai.com/news/economy/',
            'http://www.yicai.com/news/well-being/'
        ]
        for url in base_urls:
            request = Request(url, callback=self.parse_page)
            requests.append(request)
        for keyword in keywords:
            for i in (4,7):
                request = Request('http://www.yicai.com/api/ajax/NsList/'+str(i)+keyword, callback=self.parse_page)
                requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//dd')
        for p in news:
            date=''.join(p.xpath('h4/span/text()').extract()).replace(u'-',u'').replace(u':',u'').replace(u' ',u'')
            if self.yesterday in date:
                link=''.join(p.xpath('h3/a/@href').extract())
                title=p.xpath('h3/a/text()').extract()
                yield Request(link, callback=lambda response,title_=title,date_=date: self.parse_news(response,title_,date_))

    def parse_news(self,response,title_,date_):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        item['title'] = title_
        item['date'] = date_
        self.get_source(response, item)
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
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="m-text"]/p')
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
