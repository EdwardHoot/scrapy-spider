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

class CbtnetSpider(CrawlSpider):
    name='cbtnet'
    source='中时网'
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday

    def start_requests(self):
        base_urls=(
            'http://www.cbt.com.cn/cjrw/sjmj/index',
            'http://www.cbt.com.cn/cjrw/qylx/index',
            'http://www.cbt.com.cn/cjrw/jjxr/index',
            'http://www.cbt.com.cn/cjrw/zyjlr/index',
            'http://www.cbt.com.cn/sszx/index',
            'http://www.cbt.com.cn/myjj/sjfy/index',
            'http://www.cbt.com.cn/myjj/zsys/index',
            'http://www.cbt.com.cn/myjj/fzwq/index',
            'http://www.cbt.com.cn/myjj/qc/index',
            'http://www.cbt.com.cn/zcjd/zdzc/index',
            'http://www.cbt.com.cn/zcjd/zcry/index',
            'http://www.cbt.com.cn/zcjd/zcjd/index',
            'http://www.cbt.com.cn/zcjd/ckfc/index',
            'http://www.cbt.com.cn/zcjd/zyjl/index',
            'http://www.cbt.com.cn/jrkd/yh/index',
            'http://www.cbt.com.cn/zhtx/gsl/index',
            'http://www.cbt.com.cn/zhtx/lykzg/index'
        )

        requests = []

        for url in base_urls:
            request = Request(url+'.html', callback=self.parse_page)
            requests.append(request)

        for url in base_urls:
            for i in range(2,2):
                request = Request(url+'_'+str(i) + '.html', callback=self.parse_page)
                requests.append(request)

        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//a[@class="neiyediv_box_xun"]')
        for p in news:
            date=p.xpath('div[@class="neiyediv_box_div"]/div[@class="neiyediv_box_text"]/div[@class="neiyediv_box_date"]/span[@class="neiyediv_box_time"]/text()').extract()
            if self.yesterday in ''.join(date).replace(u'-',u''):
                link=''.join(p.xpath('@href').extract())
                yield Request(link, callback=self.parse_news)

    def parse_news(self,response):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        self.get_source(response, item)
        self.get_title(response, item)
        self.get_date(response, item)
        self.get_body(response, item)
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
        title=response.xpath('//div[@class="tpxwxq_title"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date=response.xpath('//span[@class="from_date"]/text()').extract()
        if date:
            item['date']=''.join(date).replace(u'-',u'').replace(u':',u'').replace(u' ',u'').strip()
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="neirong"]')
        if not paras:
            paras = response.xpath('//div[@class="neirong"]')
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
