#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class SznewsSpider(CrawlSpider):
    name='sznews'
    source = "深圳新闻网"
    allowed_domains = ["sznews.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m/%d')
    reg=yesterday
    start_urls = [
        'http://www.sznews.com/banking/node_177246.htm/',
        'http://www.sznews.com/banking/node_177247.htm/',
        'http://www.sznews.com/banking/node_177249.htm/'
    ]
    rules=(
        Rule(LinkExtractor(allow='banking/content/'+reg),callback="parse_news",follow=True),
        # Rule(LinkExtractor(allow='_[0-9].htm'))
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
        title = response.xpath('//h1[@class="h1-news"]/text()').extract()
        if not title:
            title = response.xpath('//h1[@class="con_title"]/text()').extract()
        if not title:
            title = response.xpath('//div[@id="PrintTxt"]/h2/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@class="fs18 r share-date"]/text()').extract()
        if not date:
            date=response.xpath('//div[@id="pubtime_baidu"]/text()').extract()
        if not date:
            date = response.xpath('//div[@class="con_arc_info"]/text()').extract()
        if date:
            item['date']=''.join(''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()[:12])+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="article-content cf new_txt"]/p')
        if not paras:
            paras = response.xpath('//div[@class="new_txt"]/p')
        if not paras:
            paras = response.xpath('//div[@class="con_arc_content"]/p')
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
