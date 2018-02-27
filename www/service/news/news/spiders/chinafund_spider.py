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

class ChinafundSpider(CrawlSpider):
    name = 'chinafund'
    source = "中国基金网"
    allowed_domains = ["chinafund.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')

    def start_requests(self):
        start_urls=(
            'http://www.chinafund.cn/tree/minlist/index.php?action=xwzx',
            'http://www.chinafund.cn/tree/minlist/index.php?action=xwzx_2.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=xwzx_3.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjgg',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjgg_2.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjgg_3.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjgg_4.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjzx',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjzx_2.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjzx_3.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjzx_4.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=cjzx',
            'http://www.chinafund.cn/tree/minlist/index.php?action=mjls',
            'http://www.chinafund.cn/tree/minlist/index.php?action=mjls_2.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=kfjj',
            'http://www.chinafund.cn/tree/minlist/index.php?action=fbjj',
            'http://www.chinafund.cn/tree/minlist/index.php?action=hbjj',
            'http://www.chinafund.cn/tree/minlist/index.php?action=pjbg',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjyw',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjyw_2.html',
            'http://www.chinafund.cn/tree/minlist/index.php?action=gdxw',
            'http://www.chinafund.cn/tree/minlist/index.php?action=gdxw_2',
            'http://www.chinafund.cn/tree/minlist/index.php?action=gdxw_3',
            'http://www.chinafund.cn/tree/minlist/index.php?action=gjzx',
            'http://www.chinafund.cn/tree/minlist/index.php?action=zjzx',
            'http://www.chinafund.cn/tree/minlist/index.php?action=hjzx',
            'http://www.chinafund.cn/tree/minlist/index.php?action=fjzx',
            'http://www.chinafund.cn/tree/minlist/index.php?action=qdqf',
            'http://www.chinafund.cn/tree/minlist/index.php?action=smjj',
            'http://www.chinafund.cn/tree/minlist/index.php?action=sbbx',
            'http://www.chinafund.cn/tree/minlist/index.php?action=zhnj',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jjbg',
            'http://www.chinafund.cn/tree/minlist/index.php?action=jgbg'
        )
        requests = []

        for url in start_urls:
            request = Request(url, callback=self.parse_page)
            requests.append(request)

        # for url in base_urls:
        #     for i in range(2,2100):
        #         request = Request(url+ str(i)+'.html', callback=self.parse_page)
        #         requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//li')
        for p in news:
            date=''.join(p.xpath('span/text()').extract())
            if date and self.yesterday in date:
                link=''.join(p.xpath('a/@href').extract())
                yield Request('http://www.chinafund.cn'+link, callback=self.parse_news)

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
        title=response.xpath('//div[@id="title"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@id="time"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()[:14]
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="news_text"]/p')

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
