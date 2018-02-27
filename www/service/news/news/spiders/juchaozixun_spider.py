#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
import urllib
import os


class JrjSpider(CrawlSpider):
    name='juchaozixun'
    source = "巨潮资讯网"
    allowed_domains = ["cninfo.com.cn"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')


    def getHtml(url):
        page = urllib.urlopen(url)
        html = page.read()
        return html

    def getImg(html):
        direct = '/Users/hupeng/Downloads/gbd_spider/www/service/news/files/juchaozixun'

        yesterday = datetime.date.today()
        yesterday2 = yesterday.strftime('%Y-%m-%d')
        yesterdayname = yesterday.strftime('%Y%m%d')
        os.mkdir(direct+'/'+str(yesterdayname))
        reg = r'href="/cninfo-new/disclosure/szse/bulletin_detail/true(.*)?announceTime='
        regtime = r'href="/cninfo-new/disclosure/szse/bulletin_detail/true(.*)?announceTime=(.*)" target="_blank"'
        imgre = re.compile(reg)
        timere = re.compile(regtime)
        imglist = re.findall(imgre, html)
        urllist = re.findall(timere, html)
        x = 0
        for imgurl in imglist:
            if urllist[x][1]== str(yesterday2):
                imgurl2 = 'http://www.cninfo.com.cn/finalpage/' + str(yesterday2) + imgurl[:-1] + '.PDF'
                print imgurl2
                urllib.urlretrieve(imgurl2, direct+ '/'+str(yesterdayname)+'/%s.pdf' % x)
                x += 1
            else:
                x += 1
                continue

    url = 'http://www.cninfo.com.cn/cninfo-new/index'
    html = getHtml(url)
    getImg(html)



