# -*- coding:utf-8 -*-
"""
download decorator
"""
import functools
import os, sys, time
from models import TaskRunningLog
from transwarp.web import ctx
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


def download_json_file(func):
    @functools.wraps(func)
    def weaper(*args, **kwargs):
        try:
            year, month = tushare_data_util.get_current_year_month()
            dirpath = path + '/' + str(year) + '-' + str(month)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            else:
                pass
            if len(args) > 0:
                dirpath = dirpath + '/' + str(args[0]) + 'y' + str(args[1]) + 'q'
                desc = '%s year %s quarter %s file download starting...' % (str(args[0]), str(args[1]), func.__name__[4:] + '.json')
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                else:
                    pass
            else:
                desc = '%s file download starting...' % (func.__name__[4:] + '.json')
            logger.debug(desc)
            uid = ctx.request.user.id
            uname = ctx.request.user.name
            df = func(*args, **kwargs)
            df.to_json(dirpath + '/' + func.__name__[4:] + '.json', orient='split')
            task_log = TaskRunningLog(user_id=uid, running_task_status='S', task_id='fundamental_datas_job', description=desc, created_by=uname, updated_by=uname)
            task_log.insert()
            logger.debug('%s file download end...' % (func.__name__[4:] + '.json'))
        except:
            info = sys.exc_info()
            desc = desc + ' but some errors between downloading files,the details:' + str(info[0]) + ':' + str(info[1])
            logger.exception(desc)
            task_log = TaskRunningLog(user_id=uid, running_task_status='E', task_id='fundamental_datas_job', description=desc, created_by=uname, updated_by=uname)
            task_log.insert()
        return df
    return weaper


def download_options_json_file(func):
    @functools.wraps(func)
    def weaper(*args, **kwargs):
        try:
            logger.debug('%s file download starting...' % (func.__name__[4:] + '.json'))
            df = func(*args, **kwargs)
            df.to_json(path + '/' + func.__name__[4:] + '.json', orient='split')
            logger.debug('%s file download end...' % (func.__name__[4:] + '.json'))
        except:
            logger.exception('some errors between downloading files,the details:')
        return df
    return weaper


def download_stocks_json_file(func):
    @functools.wraps(func)
    def weaper(*args, **kwargs):
        try:
            year, month = tushare_data_util.get_current_year_month()
            dirpath = path + '/' + str(year) + '-' + str(month)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            else:
                pass
            dirpath = dirpath + '/' + func.__name__[4:]
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            else:
                pass
            desc = '%s file download starting...' % (args[0] + '.json')
            logger.debug(desc)
            df = func(*args, **kwargs)
            df.to_json(dirpath + '/' + args[0] + '.json', orient='split')
            task_log = TaskRunningLog(running_task_status='S', task_id='stock_deal_data_job', description=desc)
            task_log.insert()
            logger.debug('%s file download end...' % (args[0] + '.json'))
        except:
            info = sys.exc_info()
            desc = ' but some errors between downloading files,the details:' + str(info[0]) + ':' + str(info[1])
            logger.exception(desc)
            task_log = TaskRunningLog(running_task_status='E', task_id='stock_deal_data_job', description=desc)
            task_log.insert()
        return df
    return weaper


def download_stocks_csv_file(func):
    @functools.wraps(func)
    def weaper(*args, **kwargs):
        try:
            year, month = tushare_data_util.get_current_year_month()
            dirpath = path + '/' + str(year) + '-' + str(month)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            else:
                pass
            dirpath = dirpath + '/' + func.__name__[4:]
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            else:
                pass
            logger.debug('%s file download starting...' % (args[0] + '.csv'))
            df = func(*args, **kwargs)
            df.to_csv(dirpath + '/' + args[0] + '.csv')
            logger.debug('%s file download end...' % (args[0] + '.csv'))
        except:
            logger.exception('some errors between downloading files,the details:')
        return df
    return weaper


def download_classification_json_file(func):
    @functools.wraps(func)
    def weaper(*args, **kwargs):
        try:
            year, month = tushare_data_util.get_current_year_month()
            dirpath = path + '/' + str(year) + '-' + str(month) + '/classifications'
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            else:
                pass
            uid = ctx.request.user.id
            uname = ctx.request.user.name
            desc = '%s file download starting...' % (func.__name__[4:] + '.json')
            logger.debug('%s file download starting...' % (func.__name__[4:] + '.json'))
            df = func(*args, **kwargs)
            df.to_json(dirpath + '/' + func.__name__[4:] + '.json', orient='split')
            task_log = TaskRunningLog(user_id=uid, running_task_status='S', task_id='stock_classification_datas_job', description=desc, created_by=uname, updated_by=uname)
            task_log.insert()
            logger.debug('%s file download end...' % (func.__name__[4:] + '.json'))
        except:
            info = sys.exc_info()
            desc = ' but some errors between downloading files,the details:' + str(info[0]) + ':' + str(info[1])
            logger.exception(desc)
            task_log = TaskRunningLog(user_id=uid, running_task_status='E', task_id='stock_classification_datas_job', description=desc, created_by=uname, updated_by=uname)
            task_log.insert()
        return df
    return weaper
