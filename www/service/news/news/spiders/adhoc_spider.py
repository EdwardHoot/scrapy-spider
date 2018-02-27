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
import logging

class AdhocSpider(CrawlSpider):
    name='adhoc'

    def start_requests(self):
        keywords=(
            "四川新闻网传媒（集团）股份有限公司","四川新闻网",
            "深圳市星源材质科技股份有限公司","星源材质",
            "森特士兴集团股份有限公司","森特士兴",
            "上海天永智能装备股份有限公司","天永装备",
            "上海丽人丽妆化妆品股份有限公司","丽人丽妆",
            "南京佳力图机房环境技术股份有限公司","佳力图",
            "浙江天宇药业股份有限公司","天宇药业",
            "如意情生物科技股份有限公司","如意情",
            "珠海派诺科技股份有限公司","派诺科技",
            "珠海元盛电子科技股份有限公司","元盛电子",
            "浙江天铁实业股份有限公司","天铁实业",
            "上海国有资产经营有限公司","上海国资管",
            "湖南华凯文化创意股份有限公司","华凯文化",
            "佛山市金银河智能装备股份有限公司","金银河",
            "伊戈尔电气股份有限公司","伊戈尔",
            "长春普华制药股份有限公司","普华制药",
            "江苏中旗作物保护股份有限公司","中旗作物",
            "青岛汇金通电力设备股份有限公司","汇金通",
            "爱柯迪股份有限公司","爱柯迪",
            "东莞金太阳研磨股份有限公司","金太阳",
            "无锡力芯微电子股份有限公司","力芯",
            "百合花集团股份有限公司","百合花",
            "北京星网宇达科技股份有限公司","星网宇达",
            "聚信国际租赁股份有限公司","聚信租赁",
            "广东新宏泽包装股份有限公司","新宏泽",
            "深圳市裕同包装科技股份有限公司","裕同包装",
            "重庆华森制药股份有限公司","华森制药",
            "镇海石化工程股份有限公司","镇海石化",
            "浙江元成园林集团股份有限公司","元成园林",
            "苏州麦迪斯顿医疗科技股份有限公司","麦迪斯顿",
            "苏州兴业材料科技股份有限公司","兴业材料",
            "欧派家居集团股份有限公司","欧派家居",
            "雷迪波尔服饰股份有限公司","雷迪波尔",
            "宁波太平鸟时尚服饰股份有限公司","太平鸟",
            "杭叉集团股份有限公司","杭叉集团",
            "杭州平治信息技术股份有限公司","平治信息",
            "海南钧达汽车饰件股份有限公司","钧达饰件",
            "广州弘亚数控机械股份有限公司","弘亚数控",
            "法兰泰克重工股份有限公司","法兰泰克",
            "福建天马科技集团股份有限公司","天马科技",
            "博天环境集团股份有限公司","博天环境",
            "广东宏川智慧物流股份有限公司","宏川智慧",
            "深圳市欣天科技股份有限公司","欣天科技",
            "浙江维康药业股份有限公司","维康药业",
            "徐州浩通新材料科技股份有限公司","浩通",
            "深圳市三诺声智联股份有限公司","三诺声智联",
            "深圳市嘉力达节能科技股份有限公司","嘉力达",
            "山东世纪天鸿文教科技股份有限公司","世纪天鸿",
            "上海洁昊环保股份有限公司","洁昊环保",
            "江苏云涌电子科技股份有限公司","云涌电子",
            "江苏利田科技股份有限公司","利田科技",
            "江苏精研科技股份有限公司","精研科技",
            "江苏华灿电讯股份有限公司","华灿电讯",
            "嘉必优生物技术（武汉）股份有限公司","嘉必优",
            "湖南科创信息技术股份有限公司","湖南科创",
            "和力辰光国际文化传媒（北京）股份有限公司","和力辰光",
            "广州市汇美时尚集团股份有限公司","汇美时尚",
            "福州瑞芯微电子股份有限公司","瑞芯",
        )
        requests = []
        for keyword in keywords:
            for i in range(751)[::50]:
                request = Request('http://news.baidu.com/ns?word='+keyword+'&cl=2&ct=0&tn=news&rn=50&ie=utf-8&bt=0&et=0&pn='+ str(i), callback=self.parse_page)
                requests.append(request)
        return requests

    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')

    def parse_page(self,response):
        news=response.xpath('//div[@class="result"]')
        logging.info('************' + response.url + '**************')
        for p in news:
            author = p.xpath('div/p/text()').extract()
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
