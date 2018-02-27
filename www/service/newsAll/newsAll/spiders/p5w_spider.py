#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class P5wSpider(CrawlSpider):
    name='p5w'
    source = "全景网"
    allowed_domains = ["p5w.net"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday
    start_urls = [
        'http://www.p5w.net/news/gncj',
        'http://www.p5w.net/news/gjcj',
        'http://www.p5w.net/news/cjxw',
        'http://www.p5w.net/news/xwpl',
        'http://www.p5w.net/news/biz',
        'http://www.p5w.net/news/cjxw/fdcy',
        'http://www.p5w.net/news/cjxw/zzyjxsbyb',
        'http://www.p5w.net/news/tech',
        'http://www.p5w.net/news/travel',
        'http://www.p5w.net/news/pgt',
        'http://www.p5w.net/news/sjqx',
        'http://www.p5w.net/news/gncj/index_2.htm',
        'http://www.p5w.net/news/gjcj/index_2.htm',
        'http://www.p5w.net/news/cjxw/index_2.htm',
        'http://www.p5w.net/news/xwpl/index_2.htm',
        'http://www.p5w.net/news/biz/index_2.htm',
        'http://www.p5w.net/news/cjxw/fdcy/index_2.htm',
        'http://www.p5w.net/news/cjxw/zzyjxsbyb/index_2.htm',
        'http://www.p5w.net/news/tech/index_2.htm',
        'http://www.p5w.net/news/travel/index_2.htm',
        'http://www.p5w.net/news/pgt/index_2.htm',
        'http://www.p5w.net/news/sjqx/index_2.htm',
        'http://www.p5w.net/news/gncj/index_3.htm',
        'http://www.p5w.net/news/gjcj/index_3.htm',
        'http://www.p5w.net/news/cjxw/index_3.htm',
        'http://www.p5w.net/news/xwpl/index_3.htm',
        'http://www.p5w.net/news/biz/index_3.htm',
        'http://www.p5w.net/news/cjxw/fdcy/index_3.htm',
        'http://www.p5w.net/news/cjxw/zzyjxsbyb/index_3.htm',
        'http://www.p5w.net/news/tech/index_3.htm',
        'http://www.p5w.net/news/travel/index_3.htm',
        'http://www.p5w.net/news/pgt/index_3.htm',
        'http://www.p5w.net/news/sjqx/index_3.htm',
        'http://www.p5w.net/news/gncj/index_4.htm',
        'http://www.p5w.net/news/gjcj/index_4.htm',
        'http://www.p5w.net/news/cjxw/index_4.htm',
        'http://www.p5w.net/news/xwpl/index_4.htm',
        'http://www.p5w.net/news/biz/index_4.htm',
        'http://www.p5w.net/news/cjxw/fdcy/index_4.htm',
        'http://www.p5w.net/news/cjxw/zzyjxsbyb/index_4.htm',
        'http://www.p5w.net/news/tech/index_4.htm',
        'http://www.p5w.net/news/travel/index_4.htm',
        'http://www.p5w.net/news/pgt/index_4.htm',
        'http://www.p5w.net/news/sjqx/index_4.htm',
        'http://www.p5w.net/news/gncj/index_5.htm',
        'http://www.p5w.net/news/gjcj/index_5.htm',
        'http://www.p5w.net/news/cjxw/index_5.htm',
        'http://www.p5w.net/news/xwpl/index_5.htm',
        'http://www.p5w.net/news/biz/index_5.htm',
        'http://www.p5w.net/news/cjxw/fdcy/index_5.htm',
        'http://www.p5w.net/news/cjxw/zzyjxsbyb/index_5.htm',
        'http://www.p5w.net/news/tech/index_5.htm',
        'http://www.p5w.net/news/travel/index_5.htm',
        'http://www.p5w.net/news/pgt/index_5.htm',
        'http://www.p5w.net/news/sjqx/index_5.htm'
    ]
    rules=(
        Rule(LinkExtractor(allow=reg), callback="parse_news", follow=True),
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
        title=response.xpath('//div[@class="newscontent_right2"]/h1/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//div[@class="content_info clearfix"]/span[1]/time/text()').extract()
        if not date:
            date = response.xpath('//span[@id="dTime"]/text()').extract()
        if date:
            item['date']=datetime.date.today().strftime('%Y')+''.join(date).replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="article_content2"]/div/p')
        if not paras:
            paras = response.xpath('//div[@class="Custom_UnionStyle"]/p')
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
