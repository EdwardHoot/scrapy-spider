#encoding: utf-8
import scrapy
import re
import uuid
import datetime
import json
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request
from scrapy.http import FormRequest

class weixinSpider(CrawlSpider):
    name='weixin'

    def start_requests(self):
        requests = []
        formdatas=[
            {
                "flag": "true",
                "uuid": "EB01B8353E170EA01E61FE8493F2B9F3",
                "nonce":"278c8b3c2",
                "xyz": "8183a81cbde12f4a92d42d9c7e103b9d"
            },#zhihedongfang
            {
                "flag": "true",
                "uuid": "01BECCEB76F7DD02773ADE53CF7AF7EB",
                "nonce": "1439a5ce1",
                "xyz": "0dd8312df050ff894a203e0c6009ab23"
            },#新浪财经
            {
                "flag": "true",
                "uuid": "0E34444173BA155BE1F4F933C391B0EE",
                "nonce": "a077c1fb3",
                "xyz": "063dfc1872b7da31c64c50d9a5062aa2"
            },
            {
                "flag": "true",
                "uuid": "83A2CA9363AA83ECB75B34ED01DC4C32",
                "nonce": "e9006563e",
                "xyz": "83bab2474de3472ab2f6bfc52909cf58"
            },
            {
                "flag": "true",
                "uuid": "79308AA211EC50D9A4012AC45B5DBAB6",
                "nonce": "4a4b424af",
                "xyz": "852de3a2049b3b8734f1b0f28d8f52d6"
            },#华尔街见闻
            {
                "flag": "true",
                "uuid": "393B3EC031E779DADF32993CFA8830EC",
                "nonce": "4c1468194",
                "xyz": "2c37873a1ff46d832b15862776ad71e1"
            },#凤凰财经
            {
                "flag": "true",
                "uuid": "DA374BBE5E132D07B500669C4238E7B1",
                "nonce": "e0770d48a",
                "xyz": "a54ecd3f638beb0dfa4563a1c18476e8"
            },#21世纪明天日报
            {
                "flag": "true",
                "uuid": "B7C02A92B0986ABE78CE31C641FBC869",
                "nonce": "f9014a8f5",
                "xyz": "da3039f7cc57bbb586e508ce44622ffd"
            },#新财富杂志
            {
                "flag": "true",
                "uuid": "35AF5558F274BC8AAB3CFE642B50391A",
                "nonce": "87f4a3fb7",
                "xyz": "ea6f0faaa12808014a779dc0b8cb1ca1"
            },#虎嗅网
            {
                "flag": "true",
                "uuid": "75C3D29DC34E702E61560035F4E3C2AB",
                "nonce": "a777bbdc6",
                "xyz": "8ccfce2ce1e3786ce4cb74b76e2fef8f"
            },#蓝鲸财经记者工作平台
            {
                "flag": "true",
                "uuid": "27ABF9FB5EE92C72D6673FB6C96C0D0A",
                "nonce": "8e9d52972",
                "xyz": "09aaa590ec70b85a5a8b1b69ffc974dd"
            },#二十一世纪商业评论
            {
                "flag": "true",
                "uuid": "3A116B3B86DC701A5F11ABDF2F8EFD2D",
                "nonce": "a092ba609",
                "xyz": "6048992c8fdd3f180f263456d895c3c4"
            },#环球老虎财经
            {
                "flag": "true",
                "uuid": "7B3ECC8131CAF6E4BD092D43CD68D013",
                "nonce": "1b24f4b41",
                "xyz": "7900b424bda2c42fa80504d7f5e2244a"
            },#跑赢大盘的王者
            {
                "flag": "true",
                "uuid": "8A28E60E5B619BE9BA99610571532AB6",
                "nonce": "bd9e8afe7",
                "xyz": "30be873b9dfb2b163462337ca016f840"
            },#黄生看金融
            {
                "flag": "true",
                "uuid": "D61FB912A3CF726B96BFBFC51656412B",
                "nonce": "f5f688d0b",
                "xyz": "1a8b436b176b0f09ae480ab0b86d7a0c"
            },#央视财经
            {
                "flag": "true",
                "uuid": "EDFE9A57A53019CE4E0FA3F6064C13CA",
                "nonce": "a8916abcc",
                "xyz": "9452a5eaea9b6b33677ed3807e376aa9"
            },#沙黾农
            {
                "flag": "true",
                "uuid": "696C1FB88A79178655B330361BC618CD",
                "nonce": "5fb73e4c2",
                "xyz": "0a73c00603b8b2d7365f87f10f718b8f"
            },#功夫财经
            {
                "flag": "true",
                "uuid": "B5619D201F05C49F98FB0E556DD0811F",
                "nonce": "3dc36f9fb",
                "xyz": "494e538c657a0140ca7fa4b64acb432c"
            },#钱眼
            {
                "flag": "true",
                "uuid": "C15A676FF0DD06E42E91649DA2731640",
                "nonce": "21b377dde",
                "xyz": "5f95ece8cc09c934b7d61a7988c99a5b"
            },#政商内参
            {
                "flag": "true",
                "uuid": "4ACE15B94687BEDFCE16826E6B30CA8D",
                "nonce": "4b90ba4e4",
                "xyz": "7a490c8ff34ff5269d9104b92e8806b6"
            },#财经早餐
            {
                "flag": "true",
                "uuid": "7E5B5029EE71251610F0087B82D69FD1",
                "nonce": "1b7d0978c",
                "xyz": "325fec83935a39d5eb61f059feb60ed2"
            }#吴晓波频道

        ]
        url = "http://www.newrank.cn/xdnphb/detail/getAccountArticle"
        for formdata in formdatas:
            request = FormRequest(url, callback=self.parse_json, formdata=formdata)
            requests.append(request)
        return requests

    def parse_json(self, response):
        jsonBody = json.loads(response.body)
        lastestArticles = jsonBody['value']['lastestArticle']
        for dict in lastestArticles:
            yield Request(dict['url'],callback=self.parse_news)

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
        author=response.xpath('//*[@id="post-user"]/text()').extract()
        if author:
            item['source']=u'微信公众号：'+''.join(author)
    def get_title(self,response,item):
        title=response.xpath('//*[@id="activity-name"]/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self,response,item):
        date = response.xpath('//*[@id="post-date"]/text()').extract()
        if date:
            item['date'] = ''.join(date).replace('-', '')+'000000'
    def get_body(self,response,item):
        paras = response.xpath('//div[@class="rich_media_content "]/p')
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
