# -*- coding:utf-8 -*-
"""
download decorator

"""
import functools
import os, sys

parent_path = sys.path[0].split('service')[0] + '/service/common'
if parent_path not in sys.path:
    sys.path.append(parent_path)
parent_path1 = sys.path[0].split('service')[0] + '/service/loggings'
if parent_path1 not in sys.path:
    sys.path.append(parent_path1)
parent_path2 = sys.path[0].split('service')[0] + '/service/utils'
if parent_path2 not in sys.path:
    sys.path.append(parent_path2)


import mod_config
import log_processor
import tushare_data_util


logger = log_processor.get_logger(__name__)

path = mod_config.get_config("path", "path")


def task_execute_log(func):
    @functools.wraps(func)
    def weaper(*args, **kwargs):
        try:
            logger.debug('%s file download starting...' % (func.__name__[4:] + '.json'))
            df = func(*args, **kwargs)
            logger.debug('%s file download end...' % (func.__name__[4:] + '.json'))
        except:
            logger.exception('some errors between downloading files,the details:')
        return df
    return weaper