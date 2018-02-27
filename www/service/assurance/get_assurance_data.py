
# -*- coding: utf-8 -*-


import tushare as ts
import urllib, urllib2
import os
import re
from bs4 import BeautifulSoup
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding("gbk")

parent_path = sys.path[0].split('service')[0] + '/service/loggings'
parent_path1 = sys.path[0].split('service')[0] + '/service/utils'
parent_path2 = sys.path[0].split('service')[0] + '/service/common'
if parent_path not in sys.path:
    sys.path.append(parent_path)
if parent_path1 not in sys.path:
    sys.path.append(parent_path1)
if parent_path2 not in sys.path:
    sys.path.append(parent_path2)

import mod_config
import tushare_data_util
import log_processor

logger = log_processor.get_logger(__name__)
# 0.准备,形成文件名后缀
cur_date = datetime.date.today()
suffix_date = cur_date.strftime('%Y%m%d')
yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')
e_name = 'Assurance_exception' + suffix_date + '.txt'
f_e    = open(e_name,'w+')
path = mod_config.get_config("path", "path")
# 1.获取上市公司code列表,形成url列表
def get_url():
    stockCodeList = ts.get_stock_basics().name.index._data
    url_list = []
    url = 'http://money.finance.sina.com.cn/corp/go.php/vGP_Assurance/stockid/'
    for eachStock in stockCodeList:
        url_list.append(url + eachStock + '.phtml')
    return url_list, stockCodeList

# 2.对相应的网站进行数据爬虫,获取相应信息,将数据爬成不同的list
def getAssuranceIfo():
    AssuranceList = []
    code_list = []
    url_list, stockCodeList = get_url()
    tot = len(url_list)
    cnt = 0
    for code, url in zip(stockCodeList, url_list):
        try:
            content = urllib2.urlopen(url).read()
            logger.info(code)
            cnt += 1
            logger.info(str(cnt) + '/' + str(tot))
            logger.info('-----------------')
        except Exception,e:
            logger.error(e)
            f_e.write(str(e) + '\n' )
        r = re.compile(r'<a.*?>')
        content = r.sub(' ', content)
        content = content.replace('</a>', ' ')
        content = ' '.join(content.split())
        soup = BeautifulSoup(content, from_encoding='gb18030')
        soup = soup('body')
        outlist = []
        for i in soup:
            tbody = i('tbody')
            for j in tbody:
                trow = j('tr')
                for k in trow:
                    col_name = re.findall('<strong>(.*)</strong>', str(k))
                    col_content = re.findall('<td>(.*)</td>', str(k))
                    z = re.findall('</a>(.*)</th>', str(k))
                    if len(col_name) > 0 and len(col_content) > 0:
                        out = col_name[0] + ':' + col_content[0] + '|'
                        # print(out)
                        outlist.append(out)
                Assurance = ''.join(outlist)
                Assurance = Assurance.replace('公告日期', 'flag:'+ 'Stockid:' + code + '|' + '公告日期')
                AssuranceList.append(Assurance)
                code_list.append(code)
        time.sleep(0.5)
    f_e.close()
    return AssuranceList, code_list

# 3.将每一件担保案件形成一条记录
def GetList():
    OutPut = []
    OutPutList = []
    AssuranceList, code_list = getAssuranceIfo()
    Ass_split = [i.split('flag:') for i in AssuranceList]
    for j in Ass_split:
        if len(j) > 1:
            for k in j:
                OutPut.append(k)
    for s in OutPut:
        if len(s) >= 1:
            OutPutList.append(s)
    return OutPutList

# 4.部分担保案件可能未被完全解析,这里仅保存完整的担保记录
def FinalOutPut():
    OutPutList = GetList()
    Final_Case = []
    for i in OutPutList:
        if '担保形式' in i:
            Final_Case.append(i)
    return Final_Case
#


def get_assurance_data():
    Final_Case = FinalOutPut()
    #Final_Case = ['aaaaaaaaaa']
    # 5.将前一天新增的担保记录逐条写入txt文件
    year, month = tushare_data_util.get_current_year_month()
    dirpath = path + str(year) + '-' + str(month)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    else:
        pass
    pub_date = '公告日期:' + yesterday
    assurance_dir = dirpath + '/assurance'
    if not os.path.exists(assurance_dir):
        os.makedirs(assurance_dir)
    file_name = assurance_dir + '/Assurance' + suffix_date + '.txt'
    f = open(file_name, 'w+')
    for i in Final_Case:
        if pub_date in i:
            a = i.replace('Stockid:','').replace('公告日期:','').replace('提供担保方:','').replace('获得担保方:','').replace('担保内容:','')
            b = a.replace('担保形式:','').replace('担保起始日:','').replace('担保终止日:','').replace('交易金额(万元):','').replace('币种:','')
            c = b.replace(' ','')
            item = c.split('|')
            if item[5]=='' or item[6]=='' or item[7]=='':
                f.write(c + str(0) + '\n')
            else:
                f.write(c + str(1) + '\n')
    f.close()
    tushare_data_util.zip_dir_and_delete('assurance')
    logger.info('execute assurance:tushare_data_util.upload_zip_files()...')
    tushare_data_util.upload_zip_files('assurance')


if __name__=='__main__':
    get_assurance_data()