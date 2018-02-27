# -*- coding:utf-8 -*-
"""
get stock classified data

"""
import tushare as ts
import download_decorator
import os
import sys

parent_path = sys.path[0].split('service')[0]  + '/service/loggings'
parent_path1 = sys.path[0].split('service')[0]  + '/service/utils'
if parent_path not in sys.path:
    sys.path.append(parent_path)
if parent_path1 not in sys.path:
    sys.path.append(parent_path1)
import log_processor
import tushare_data_util

logger = log_processor.get_logger(__name__)


@download_decorator.download_classification_json_file
def get_industry_classified():
    try:
        logger.info('get get industry data starting...')
        df = ts.get_industry_classified()
        logger.info('get get industry data end...')
    except:
        logger.exception('some errors between get industry data: ')
    return df


@download_decorator.download_classification_json_file
def get_concept_classified():
    try:
        logger.info('get concept data starting...')
        df = ts.get_concept_classified()
        logger.info('get concept data end...')
    except:
        logger.exception('some errors between get concept data end...')

    return df


@download_decorator.download_classification_json_file
def get_area_classified():
    try:
        logger.info('get area data starting...')
        df = ts.get_area_classified()
        logger.info('get area data end...')
    except:
        logger.exception('some errors between get area data end...')
    return df


@download_decorator.download_classification_json_file
def get_sme_classified():
    try:
        logger.info('get sme data starting...')
        df = ts.get_sme_classified()
        logger.info('get sme data end...')
    except:
        logger.exception('some errors between get sme data end...')
    return df


@download_decorator.download_classification_json_file
def get_gem_classified():
    try:
        logger.info('get gem data starting...')
        df = ts.get_gem_classified()
        logger.info('get gem data end...')
    except:
        logger.exception('some errors between get gem data end...')
    return df


@download_decorator.download_classification_json_file
def get_st_classified():
    try:
        logger.info('get st data starting...')
        df = ts.get_st_classified()
        logger.info('get st data end...')
    except:
        logger.exception('some errors between get st data end...')
    return df


@download_decorator.download_classification_json_file
def get_hs300s():
    try:
        logger.info('get hs300s data starting...')
        df = ts.get_hs300s()
        logger.info('get hs300s data end...')
    except:
        logger.exception('some errors between get hs300s data end...')
    return df


@download_decorator.download_classification_json_file
def get_sz50s():
    try:
        logger.info('get sz50s data starting...')
        df = ts.get_sz50s()
        logger.info('get sz50s data end...')
    except:
        logger.exception('some errors between get sz50s data end...')
    return df


@download_decorator.download_classification_json_file
def get_zz500s():
    try:
        logger.info('get zz500s data starting...')
        df = ts.get_zz500s()
        logger.info('get zz500s data end...')
    except:
        logger.exception('some errors between get zz500s data end...')
    return df


@download_decorator.download_classification_json_file
def get_terminated():
    try:
        logger.info('get terminated data starting...')
        df = ts.get_terminated()
        logger.info('get terminated data end...')
    except:
        logger.exception('some errors between get terminated data end...')
    return df


@download_decorator.download_classification_json_file
def get_suspended():
    try:
        logger.info('get suspended data starting...')
        df = ts.get_suspended()
        logger.info('get suspended data end...')
    except:
        logger.exception('some errors between get suspended data end...')
    return df


def get_stock_classification_datas():
    logger.info('Run task %s (%s)...' % ('get_stock_classification_datas', os.getpid()))
    get_industry_classified()
    get_concept_classified()
    get_area_classified()
    get_gem_classified()
    get_hs300s()
    get_sme_classified()
    get_st_classified()
    get_suspended()
    get_sz50s()
    get_terminated()
    logger.info('execute classifications:tushare_data_util.zip_dir_and_delete()...')
    tushare_data_util.zip_dir_and_delete('classifications')
    logger.info('execute classifications:tushare_data_util.upload_zip_files()...')
    tushare_data_util.upload_zip_files('classifications')

if __name__ == '__main__':
    get_industry_classified()
    get_concept_classified()
    get_area_classified()
    get_gem_classified()
    get_hs300s()
    get_sme_classified()
    get_st_classified()
    get_suspended()
    get_sz50s()
    get_terminated()
