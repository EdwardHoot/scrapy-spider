# -*- coding:utf-8 -*-
"""
get path

"""
import ConfigParser
import os
import sys

parent_path = sys.path[0].split('service')[0] + '/service/loggings'
if parent_path not in sys.path:
    sys.path.append(parent_path)


import log_processor


logger = log_processor.get_logger(__name__)


def get_config(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/system.conf'
    config.read(path)
    record = {'config file path': path, 'section': section, 'key': key}
    logger.info(record)
    return config.get(section, key)

if __name__ == '__main__':
    path = os.path.split(os.path.realpath(__file__))[0] + '/system.conf'

    print sys.path[0].split('service')