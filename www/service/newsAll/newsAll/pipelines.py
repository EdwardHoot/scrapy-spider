# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime,sys,os
from scrapy import signals
from newsAll.TsvItemExporter import TsvItemExporter

class NewsAllPipeline(object):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')

    def __init__(self):
        pass
    @classmethod
    def from_crawler(cls,crawler):
        pipeline=cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline
    def spider_opened(self,spider):
        self.file=open('files/'+self.yesterday+'/'+self.yesterday+spider.name+'.txt','wb')
        self.exporter=TsvItemExporter(self.file)
        self.exporter.start_exporting()
    def spider_closed(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
        fin = open('files/'+self.yesterday+'/'+self.yesterday+spider.name+'.txt')
        a = fin.readlines()
        fout = open('files/'+self.yesterday+'/'+self.yesterday+spider.name+'.txt', 'wb')
        b = ''.join(a[1:])
        fout.write(b)
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

