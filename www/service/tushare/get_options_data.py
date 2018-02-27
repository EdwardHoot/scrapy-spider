# -*- coding:utf-8 -*-
"""
get Options data

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

tushare_data_util.set_wmcloud_token(ts)


@download_decorator.download_options_json_file
def get_Options(**params):
    try:
        logger.info('get options data starting...')
        fd = ts.Options()
        df = fd.Opt(ontractStatus='L,DE', field='optID,secShortName,varShortName,listDate')
        logger.info('get options data end...')
    except:
        logger.exception('some errors between get options data: ')
    return df


@download_decorator.download_json_file
def get_IVs(**params):
    try:
        logger.info('get IV data starting...')
        iv = ts.IV()
        df = iv.DerIv(**params)
        logger.info('get IV data end...')
    except:
        logger.exception('some errors between get IV data: ')
    return df


if __name__ == '__main__':
    print ts.get_token()
    fd = ts.Options()
    df = fd.Opt(contractStatus='L,DE', field='optID,secShortName,varShortName,listDate')
    print df
    mkt = ts.Market()
    df = mkt.TickRTSnapshot(securityID='000001.XSHE')
