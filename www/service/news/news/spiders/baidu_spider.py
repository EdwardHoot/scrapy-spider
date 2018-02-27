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

class BaiduSpider(CrawlSpider):
    name='baidu'
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    reg=yesterday

    def start_requests(self):
        keywords=(
            '公司',
            '财经新闻',
            '科技',
            '抵押',
            '担保',
            '竞争',
            '应收账款',
            '资金占用',
            '客户',
            '供应商',
            '中标',
            '合同',
            '融资租赁',
        )

        corps=(
            '中山市金马游艺机有限公司', '金马游艺机',
            '吉林市长吉图投资有限公司', '长吉图投资',
            '深圳市天图投资管理股份有限公司', '天图投资', '天图',
            '陕西省交通建设集团公司', '陕西省交通建设', '陕西省交建', '陕西交建',
            '中天证券有限责任公司', '中天', '中天证券',
            '邦信资产管理有限公司', '邦信', '邦信资产', '邦信资管'
            '望城经开区建设开发公司', '望城经开区',
            '中山市大信酒店有限公司', '大信酒店',
            '包头市保障性住房发展建设投资有限公司', '包头保障房',
            '佛山市顺德区碧桂园地产有限公司', '桂碧园',
            '福建省闽兴医药有限公司', '闽兴', '闽兴医药',
            '上海你我贷互联网金融信息服务有限公司', '你我贷',
            '大连装备投资集团有限公司', '大连装备投资', '大连装备',
            '浙江蚂蚁小微金融服务集团有限公司', '蚂蚁小微', '小微金融', '蚂蚁金服',
            '成都东方广益投资有限公司', '东方广益',
            '珠海京投实业有限公司', '京投实业',
            '杭州也牛资产管理有限公司', '也牛', '杭州也牛',
            '内蒙古交通投资有限责任公司', '内蒙古交投', '内蒙古交通投资',
            '天津房地产集团有限公司', '天津房地产',
            '常州市武进区通利农村小额贷款股份有限公司', '通利农村小额贷款', '通利农贷',
            '佳木斯春秋航空票务有限公司','佳木斯春秋航空',
            '春秋航空股份有限公司','春秋航空',
            '万科企业股份有限公司','万科',
            '江西正邦科技股份有限公司','正邦科技',
            '万科企业集团',
            '易方达基金管理有限公司','易方达',
            '中证信用增进股份有限公司','中证信用',
            '深圳市长亮科技股份有限公司','长亮科技',
            '深圳市长亮数据技术有限公司','长亮数据',
            '文思海辉技术有限公司','文思海辉',
            '中科软科技股份有限公司','中科软科技',
            '软通动力信息技术（集团）有限公司','软通动力','软通'
            '软通动力控股有限公司',
            '杭州可续家居有限公司','可续家居','木智工坊',
            '蚂蚁金融服务集团',
            '深圳广田集团股份有限公司','广田',
            '北京京东金融科技控股有限公司','京东金融',
            '北控水务',
            '望城经开',
            '中铁二局','中铁工业',
            '中软国际科技服务有限公司', '中软','中软国际',
            '宇信易诚科技有限公司','宇信易诚',
            '北京文思海科技有限公司','文思海',
            '深圳市长亮保泰信息科技有限公司','长亮保泰',
            '南京帆软软件有限公司','南京帆软',
            '北京永洪商智科技有限公司','永洪商智',
            '广州元曜软件有限公司','元曜软件',
            '北京先进数通信息技术股份公司','先进数通',
            '乐视网信息技术(北京)股份有限公司','乐视',
            '中节能风力发电股份有限公司','中节能',
            '珈伟股份',
        )

        requests = []
        for keyword in keywords:
            for i in range(1001)[::50]:
                request = Request('http://news.baidu.com/ns?word='+keyword+'&cl=2&ct=0&tn=news&rn=50&ie=utf-8&bt=0&et=0&pn='+ str(i), callback=self.parse_page)
                requests.append(request)

        for corp in corps:
            for i in range(31)[::30]:
                request = Request('http://news.baidu.com/ns?word='+corp+'&cl=2&ct=0&tn=news&rn=50&ie=utf-8&bt=0&et=0&pn='+ str(i), callback=self.parse_page)
                requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//div[@class="result"]')
        for p in news:
            author = p.xpath('div/p/text()').extract()
            if self.yesterday in ''.join(author)[-17:].replace(u'年',u'').replace(u'月',u'').replace(u'日',u''):
                link=''.join(p.xpath('h3/a/@href').extract())
                source=''.join(author)[:-19]
                date=''.join(''.join(author)[-17:]).replace(u'年',u'').replace(u'月',u'').replace(u'日',u'').replace(u':',u'').replace(u' ',u'').strip()+'00'
                yield Request(link, callback=lambda response, source_=source,date_=date: self.parse_news(response,source_,date_))

    def parse_news(self,response,source_,date_):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        item['source']=source_
        self.get_title(response,item)
        item['date'] = date_
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
    def get_title(self,response,item):
        title=response.xpath('//title/text()').extract()
        if title:
            item['title']=''.join(title).strip()
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
