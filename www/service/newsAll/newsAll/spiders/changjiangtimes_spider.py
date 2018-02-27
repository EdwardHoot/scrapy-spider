# encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

class ChangjiangtimesSpider(CrawlSpider):
    name = 'changjiangtimes'
    source = "长江商报"
    allowed_domains = ["changjiangtimes.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')

    def start_requests(self):
        start_urls = (
            'http://www.changjiangtimes.com/c/money/',
            'http://www.changjiangtimes.com/c/4359/',
            'http://www.changjiangtimes.com/c/stock/',
            'http://www.changjiangtimes.com/c/4355/',
            'http://www.changjiangtimes.com/c/4351/',
            'http://www.changjiangtimes.com/c/4354/',
            'http://www.changjiangtimes.com/c/4353/',
            'http://www.changjiangtimes.com/c/IT/',
            'http://www.changjiangtimes.com/c/fdc/',
            'http://www.changjiangtimes.com/c/4352/',
            'http://www.changjiangtimes.com/c/4329/',
            'http://www.changjiangtimes.com/c/idol/',
            'http://www.changjiangtimes.com/c/pl/',
            'http://www.changjiangtimes.com/c/shizheng/',
            'http://www.changjiangtimes.com/c/shehui/',
            'http://www.changjiangtimes.com/c/minsheng/',
            'http://www.changjiangtimes.com/c/world/',
            'http://www.changjiangtimes.com/c/4371/'
        )
        requests = []

        for url in start_urls:
            request = Request(url, callback=self.parse_page)
            requests.append(request)

        # for url in base_urls:
        #     for i in range(2,10):
        #         request = Request(url+ str(i)+'.html', callback=self.parse_page)
        #         requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self, response):
        news = response.xpath('//div[@class="limain"]')
        for p in news:
            date = ''.join(p.xpath('a/p[@class="pdate"]/text()').extract())
            if date and self.yesterday in date:
                link = ''.join(p.xpath('a/@href').extract())
                yield Request('http://www.changjiangtimes.com'+link, callback=self.parse_news)

    def parse_news(self, response):
        item = GenericItem()
        self.get_id(response, item)
        self.get_url(response, item)
        self.get_source(response, item)
        self.get_title(response, item)
        self.get_date(response, item)
        self.get_body(response, item)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!remenber to Retrun Item after parse
        return item

    def get_id(self, response, item):
        id = uuid.uuid4()
        if id:
            item['id'] = id

    def get_url(self, response, item):
        news_url = response.url
        if news_url:
            item['url'] = news_url

    def get_source(self, response, item):
        source = self.source
        if source:
            item['source'] = source

    def get_title(self, response, item):
        title = response.xpath('//div[@class="px6"]/h1/text()').extract()
        if title:
            item['title'] = ''.join(title).strip()

    def get_date(self, response, item):
        date = response.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        if date:
            item['date'] = ''.join(date).replace(u'-', u'').replace(u':', u'').replace(u' ', u'').strip()

    def get_body(self, response, item):
        paras = response.xpath('//div[@class="c_zw"]/p')

        news_body = ''
        for p in paras:
            data = p.xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    #   print entry.encode('utf-8')
                    body += line.strip()
                news_body += body + '_|_'
        item['body'] = news_body.replace('_|__|_', '_|_')

