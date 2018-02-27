# -*- coding:utf-8 -*-
"""
logger processor
Created on 2016/08/29
@author: zhuweifeng641
@group : pingan
"""
import logging
import logging.config
import os

path = os.path.split(os.path.realpath(__file__))[0] + '/loggings.conf.dev'
logging.config.fileConfig(path)


def get_logger(name):
    return logging.getLogger(name)

if __name__ == '__main__':
    print path