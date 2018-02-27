import time,datetime
import os
import sys
import zipfile
import shutil
import urllib2

parent_path = sys.path[0].split('service')[0] + '/service/common'
parent_path1 = sys.path[0].split('service')[0] + '/service/loggings'
if parent_path not in sys.path:
    sys.path.append(parent_path)
if parent_path1 not in sys.path:
    sys.path.append(parent_path1)

import mod_config
import log_processor

logger = log_processor.get_logger(__name__)
path = mod_config.get_config("path", "path")


def get_quarter_by_month(month):
    if month in (1, 2, 3):
        return 1
    elif month in (4, 5, 6):
        return 2
    elif month in (7, 8, 9):
        return 3
    else:
        return 4


def get_history_year_quarters():
    year_quarter_map =[]
    year, month = get_current_year_month()
    for i in range(1991, year):
        for j in range(1, 5):
            year_quarter_map.append(str(i) + ':' + str(j))
    return year_quarter_map


def get_year_quarter(s):
    return int(s.split(':')[0]), int(s.split(':')[1])


def get_current_year_month():
    year = int(time.strftime('%Y', time.localtime(time.time())))
    month = int(time.strftime('%m', time.localtime(time.time())))
    return year, month

def get_yesterdasy():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    return yesterday



def set_wmcloud_token(ts):
    ts.set_token(mod_config.get_config('wmcloud','token'))


def zip_dir(dirname, zipfilename):
    filelist  = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)
    zf.close()


def zip_dir_and_delete(dir_name):
    year, month = get_current_year_month()
    src_path = path + str(year) + '-' + str(month) + '/' + dir_name
    if not os.listdir(src_path) == []:
        zip_dir(src_path, src_path + '.zip')
        shutil.rmtree(src_path)
    else:
        shutil.rmtree(src_path)

def zip_daily_dir_and_delete():
    yesterday=get_yesterdasy()
    today = datetime.date.today().strftime('%Y%m%d')
    src_path = sys.path[0].split('service')[0] + '/service/news/files/'+yesterday
    if not os.listdir(src_path) == []:
        f = zipfile.ZipFile(sys.path[0].split('service')[0] + '/service/news/files/'+today+'.zip', 'w', zipfile.ZIP_DEFLATED)
        f.write(src_path+'.txt',yesterday+'.txt')
        f.close()
        shutil.rmtree(sys.path[0].split('service')[0] + '/service/news/files/'+yesterday)
    else:
        shutil.rmtree(sys.path[0].split('service')[0] + '/service/news/files/'+yesterday)

def upload_zip_files(dir_name):
    year, month = get_current_year_month()
    file_path = path + str(year) + '-' + str(month) + '/' + dir_name + '.zip'
    url = mod_config.get_config('post_url', 'url') + '?file_path=' + file_path + '&file_name=' + dir_name
    logger.info(url)
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    logger.info(res)

def upload_daily_files():
    today = datetime.date.today().strftime('%Y%m%d')
    file_path = sys.path[0].split('service')[0] + '/service/news/files/'+today+'.zip'
    url = mod_config.get_config('post_url', 'url') + '?file_path=' + file_path + '&file_name=' + today
    logger.info(url)
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    logger.info(res)


if __name__ == '__main__':
    f = '/home/zhuweifeng641/PycharmProjects/gbd-gface-spider/spider-files/2016-10/classifications'
    #zip_dir(f, '/home/zhuweifeng641/PycharmProjects/gbd-gface-spider/spider-files/2016-10/classifications.zip')
    #zip_dir_and_delete('classifications');
    upload_zip_files('assurance');
