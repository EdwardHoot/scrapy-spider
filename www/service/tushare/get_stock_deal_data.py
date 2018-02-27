# -*- coding:utf-8 -*-
"""
get stock deal data

"""
import tushare as ts
import download_decorator
import os
import sys
import threading

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
import log_processor
import tushare_data_util

logger = log_processor.get_logger(__name__)
path = mod_config.get_config("path", "path")


@download_decorator.download_stocks_json_file
def get_hist_data(stock_code, **params):
    try:
        logger.info('get get history stocks data starting...')
        df = ts.get_hist_data(stock_code, **params)
        logger.info('get get history stocks data end...')
    except:
        logger.exception('some errors between get history stocks data: ')
    return df


@download_decorator.download_json_file
def get_stock_basics(**params):
    try:
        logger.info('get stock basics data starting...')
        df = ts.get_stock_basics(**params)
        logger.info('get stock basics data end...')
    except:
        logger.exception('some errors between stock basics data end...')

    return df


@download_decorator.download_json_file
def get_today_all():
    try:
        logger.info('get today all data starting...')
        df = ts.get_today_all()
        logger.info('get today all data end...')
    except:
        logger.exception('some errors between get today all data end...')
    return df


@download_decorator.download_stocks_csv_file
def get_tick_data(stock_code, **params):
    try:
        logger.info('get tick data starting...')
        df = ts.get_tick_data(stock_code, **params)
        logger.info('get tick data end...')
    except:
        logger.exception('some errors between get tick data end...')
    return df


@download_decorator.download_stocks_json_file
def get_realtime_quotes(*params):
    try:
        logger.info('get realtime quotes data starting...')
        df = ts.get_realtime_quotes(*params)
        logger.info('get realtime quotes data end...')
    except:
        logger.exception('some errors between get realtime quotes data end...')
    return df


@download_decorator.download_stocks_json_file
def get_today_ticks(stock_code, **params):
    try:
        logger.info('get today ticks data starting...')
        df = ts.get_today_ticks(stock_code, **params)
        logger.info('get today ticks data end...')
    except:
        logger.exception('some errors between get today ticks data end...')
    return df


@download_decorator.download_json_file
def get_index():
    try:
        logger.info('get index data starting...')
        df = ts.get_index()
        logger.info('get index data end...')
    except:
        logger.exception('some errors between get index data end...')
    return df


@download_decorator.download_stocks_csv_file
def get_sina_dd(stock_code, **params):
    try:
        logger.info('get sina DD data starting...')
        df = ts.get_sina_dd(stock_code,  **params)
        logger.info('get sina DD data end...')
    except:
        logger.exception('some errors between get sina DD data end...')
    return df


def get_stock_deal_data():
    logger.info('Run task %s (%s)...' % ('get_stock_deal_data', os.getpid()))
    get_stock_basics()
    get_index()
    get_today_all()
    df = ts.get_stock_basics()
    index = df.index
    for i in index:
        get_hist_data(i)
        get_realtime_quotes(i)
        get_today_ticks(i)
        get_sina_dd(i)
        get_tick_data(i)
    dir_names = ('hist_data', 'realtime_quotes', 'today_ticks', 'sina_dd', 'tick_data')
    for dn in dir_names:
        tushare_data_util.zip_dir_and_delete(dn)
        logger.info('execute ' + dn + ':tushare_data_util.upload_zip_files()...')
        tushare_data_util.upload_zip_files(dn)


def get_stock_hist_data(index_start, index_end):
    logger.info('Run task %s (%s)...' % ('get_stock_hist_data', os.getpid()))
    df = ts.get_stock_basics()
    index = df.index
    for i in index[index_start:index_end]:
        get_hist_data(i)


def get_stock_hist_data_multithreading():
    df = ts.get_stock_basics()
    index = df.index
    count = len(index)
    threads = []
    t1 = threading.Thread(target=get_stock_hist_data, args=(0, 600,))
    threads.append(t1)
    t2 = threading.Thread(target=get_stock_hist_data, args=(601, 1200,))
    threads.append(t2)
    t3 = threading.Thread(target=get_stock_hist_data, args=(1201, 1800,))
    threads.append(t3)
    t4 = threading.Thread(target=get_stock_hist_data, args=(1801, 2400,))
    threads.append(t4)
    t5 = threading.Thread(target=get_stock_hist_data, args=(2401, count))
    threads.append(t5)
    for t in threads:
        t.setDaemon(True)
        t.start()
        t.join()
    tushare_data_util.zip_dir_and_delete('hist_data')
    logger.info('execute hist_data:tushare_data_util.upload_zip_files()...')
    #tushare_data_util.upload_zip_files('hist_data')

if __name__ == '__main__':
    get_stock_hist_data_multithreading()