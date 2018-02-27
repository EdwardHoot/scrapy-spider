# -*- coding:utf-8 -*-
"""
get 基本面数据

"""
import os
import sys
import tushare as ts
import download_decorator

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


@download_decorator.download_json_file
def get_stock_basics():
    try:
        logger.info('get get stocks data starting...')
        df = ts.get_stock_basics()
        logger.info('get get stocks data end...')
    except:
        logger.exception('some errors between get stocks data: ')
    return df


@download_decorator.download_json_file
def get_report_data(year,quarter):
    try:
        logger.info('get %s year %s quarter report data starting...'%(year, quarter))
        df = ts.get_report_data(year, quarter)
        logger.info('get %s year %s quarter report data end...'%(year, quarter))
    except:
        logger.exception('some errors between get %s year %s quarter report data end...'%(year,quarter))

    return df


@download_decorator.download_json_file
def get_profit_data(year, quarter):
    try:
        logger.info('get %s year %s quarter profit data starting...' % (year, quarter))
        df = ts.get_profit_data(year, quarter)
        logger.info('get %s year %s quarter profit data end...' % (year, quarter))
    except:
        logger.exception('some errors between get %s year %s quarter profit data end...' % (year, quarter))
    return df


@download_decorator.download_json_file
def get_operation_data(year, quarter):
    try:
        logger.info('get %s year %s quarter operation data starting...' % (year, quarter))
        df = ts.get_operation_data(year, quarter)
        logger.info('get %s year %s quarter operation data end...' % (year, quarter))
    except:
        logger.exception('some errors between get %s year %s quarter operation data end...' % (year, quarter))
    return df


@download_decorator.download_json_file
def get_growth_data(year, quarter):
    try:
        logger.info('get %s year %s quarter growth data starting...' % (year, quarter))
        df = ts.get_growth_data(year, quarter)
        logger.info('get %s year %s quarter growth data end...' % (year, quarter))
    except:
        logger.exception('some errors between get %s year %s quarter growth data end...' % (year, quarter))
    return df


@download_decorator.download_json_file
def get_debtpaying_data(year, quarter):
    try:
        logger.info('get %s year %s quarter debtpaying data starting...' % (year, quarter))
        df = ts.get_debtpaying_data(year, quarter)
        logger.info('get %s year %s quarter debtpaying data end...' % (year, quarter))
    except:
        logger.exception('some errors between get %s year %s quarter debtpaying data end...' % (year, quarter))
    return df


@download_decorator.download_json_file
def get_cashflow_data(year, quarter):
    try:
        logger.info('get %s year %s quarter cashflow data starting...' % (year, quarter))
        df = ts.get_cashflow_data(year, quarter)
        logger.info('get %s year %s quarter cashflow data end...' % (year, quarter))
    except:
        logger.exception('some errors between get %s year %s quarter cashflow data end...' % (year, quarter))
    return df


def get_fundamental_data_by_month():
    try:
        logger.info('get 基本面数据 starting...')
        get_stock_basics()
        logger.info('get 基本面数据 end...')
    except:
        logger.exception('some errors between get 基本面数据:')


def get_fundamental_data_by_quarter():
    try:
        year, month = tushare_data_util.get_current_year_month()
        if month in (1, 4, 7, 10):
            quarter = int(tushare_data_util.get_quarter_by_month((lambda x: 12 if (x == 1) else (x-1))(month)))
            dir_name = str(year) + 'y' + str(quarter) + 'q'
            logger.info('get %s year %s quarter 基本面数据 starting...' % (year, quarter))
            get_cashflow_data(year, quarter)
            get_debtpaying_data(year, quarter)
            get_growth_data(year, quarter)
            get_operation_data(year, quarter)
            get_profit_data(year, quarter)
            get_report_data(year, quarter)
            tushare_data_util.zip_dir_and_delete(dir_name)
            logger.info('execute ' + dir_name + ':tushare_data_util.upload_zip_files()...')
            tushare_data_util.upload_zip_files(dir_name)
            logger.info('get %s year %s quarter 基本面数据 end...' % (year, quarter))
        else:
            pass
    except:
        logger.exception('some errors between get 基本面数据:')


def get_fundamental_datas_history():
    for s in tushare_data_util.get_history_year_quarters()[:len(tushare_data_util.get_history_year_quarters()) - 2]:
            year, quarter = tushare_data_util.get_year_quarter(s)
            dir_name = str(year) + 'y' + str(quarter) + 'q'
            try:
                logger.info('get 基本面数据 starting...')
                get_cashflow_data(year, quarter)
                get_debtpaying_data(year, quarter)
                get_growth_data(year, quarter)
                get_operation_data(year, quarter)
                get_profit_data(year, quarter)
                get_report_data(year, quarter)
                tushare_data_util.zip_dir_and_delete(dir_name)
                logger.info('execute ' + dir_name + ':tushare_data_util.upload_zip_files()...')
                tushare_data_util.upload_zip_files(dir_name)
                logger.info('get 基本面数据 end...')

            except:
                logger.exception('some errors between get 基本面数据:')


def get_fundamental_datas_now():
    logger.info('Run task %s (%s)...' % ('get_fundamental_datas', os.getpid()))
    get_fundamental_data_by_month()
    get_fundamental_data_by_quarter()

if __name__ == '__main__':
    get_fundamental_data_by_month()