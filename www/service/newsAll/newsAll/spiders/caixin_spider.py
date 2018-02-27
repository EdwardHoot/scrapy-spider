#encoding: utf-8
import scrapy
import re
import uuid
import datetime
import json
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request

class CaixinSpider(CrawlSpider):
    name='caixinall'
    source = "财新网"
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    reg=yesterday

    def start_requests(self):
        start_urls = [
            'http://tag.caixin.com/news/homeInterface.jsp?subject=100926462;100769464;100769463;100769460;100701785&start=0&picdim=_300_200&type=2&callback=jsonp1487299941749',
            'http://tag.caixin.com/news/homeInterface.jsp?subject=100300007&start=0&picdim=_75_50&callback=jsonp1487300029286',
            'http://tag.caixin.com/news/homeInterface.jsp?channel=130&start=0&picdim=_145_97&callback=jQuery172011125288244926401_1487299852386&_=1487299994511&count=',
            'http://tag.caixin.com/news/homeInterface.jsp?channel=125&start=0&picdim=_145_97&callback=jQuery17208075218858474307_1487299850285&_=1487300078535&count=',
            'http://tag.caixin.com/news/homeInterface.jsp?channel=129&start=0&picdim=_145_97&callback=jQuery17207544388244981384_1487299846414&_=1487300093979&count='
        ]
        requests=[]
        for url in start_urls:
            request = Request(url, callback=self.parse_json)
            # for i in range(2):
            #     request = Request(url + i, callback=self.parse_json)
            requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_json(self, response):
        res = ''.join(response.body).strip()
        jsonBody = json.loads(''.join(res[res.index('datas') - 2:-2]))
        datas=jsonBody['datas']
        for data in datas:
            link=data['link']
            if self.yesterday in link:
                yield Request(link, callback=self.parse_news)

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
        title=response.xpath('//*[@id="conTit"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@id="artInfo"]/text()').extract()[0]
        if date:
            item['date']=''.join(date).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()[:12]+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@id="Main_Content_Val"]/p')
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
