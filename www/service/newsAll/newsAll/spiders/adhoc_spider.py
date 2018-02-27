#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from newsAll.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request

class AdhocSpider(CrawlSpider):
    name='adhocall'

    def start_requests(self):
        keywords=(
            '中山市金马游艺机有限公司','金马游艺机',
            '吉林市长吉图投资有限公司','长吉图投资',
            '深圳市天图投资管理股份有限公司','天图投资','天图',
            '陕西省交通建设集团公司','陕西省交通建设','陕西省交建','陕西交建',
            '中天证券有限责任公司','中天','中天证券',
            '邦信资产管理有限公司','邦信','邦信资产','邦信资管'
            '望城经开区建设开发公司','望城经开区',
            '中山市大信酒店有限公司','大信酒店',
            '包头市保障性住房发展建设投资有限公司','包头保障房',
            '佛山市顺德区碧桂园地产有限公司','桂碧园',
            '福建省闽兴医药有限公司','闽兴','闽兴医药',
            '上海你我贷互联网金融信息服务有限公司','你我贷',
            '大连装备投资集团有限公司','大连装备投资','大连装备',
            '浙江蚂蚁小微金融服务集团有限公司','蚂蚁小微','小微金融','蚂蚁金服',
            '成都东方广益投资有限公司','东方广益',
            '珠海京投实业有限公司','京投实业',
            '杭州也牛资产管理有限公司','也牛','杭州也牛',
            '内蒙古交通投资有限责任公司','内蒙古交投','内蒙古交通投资',
            '天津房地产集团有限公司','天津房地产',
            '常州市武进区通利农村小额贷款股份有限公司','通利农村小额贷款','通利农贷',
        )
        requests = []
        for keyword in keywords:
            for i in range(60)[::20]:
                request = Request('http://news.baidu.com/ns?word='+keyword+'&cl=2&ct=0&tn=news&rn=20&ie=utf-8&bt=0&et=0&pn='+ str(i), callback=self.parse_page)
                requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//div[@class="result"]')
        for p in news:
            author = p.xpath('div/p/text()').extract()
            # if self.yesterday in ''.join(author)[-17:].replace(u'年',u'').replace(u'月',u'').replace(u'日',u''):
            link=''.join(p.xpath('h3/a/@href').extract())
            source=''.join(author)[:-19]
            title=p.xpath('h3/a/text()').extract()
            date=''.join(''.join(author)[-17:]).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
            yield Request(link, callback=lambda response, source_=source,title_=title,date_=date: self.parse_news(response,source_,title_,date_))

    def parse_news(self,response,source_,title_,date_):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        item['source']=source_
        item['title'] = title_
        item['date'] = date_

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
    def get_body(self,response,item):
        paras = response.xpath('//p | //span')
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
