#encoding: utf-8
import scrapy
import re
import base64
from scrapy.selector import Selector
from aperiodicity.items import StockLeaderItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class stockleadersSpider(CrawlSpider):
    name='stockleaders'
    # allowed_domains = ["sina.com.cn"]
    custom_settings = {
        "FIELDS_TO_EXPORT" : [
            'leaders'
        ]
    }

    reg='vCI_CorpManager/stockid*'
    start_urls = ['http://127.0.0.1:9000/stock']
    rules=(
        Rule(LinkExtractor(allow=reg),
        callback="parse_news",follow=True),
    )
    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')
    def parse_news(self,response):
        item = StockLeaderItem()
        self.get_leaders(response,item)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!remenber to Retrun Item after parse
        return item

    def get_leaders(self,response,item):
        news_body = ''
        line = ''
        tds=response.xpath('//td[@class="ccl"]')
        i=0
        for td in tds:
            if i%4==0:
                line += response.url[-12:-6] + '\t'
            data = td.xpath('string(.)').extract()
            if data:
                line += ''.join(data).strip()+'\t'
            if i%4==3:
                line+='\n'
                news_body+=line
                line=''
            i+=1
        item['leaders'] = news_body
