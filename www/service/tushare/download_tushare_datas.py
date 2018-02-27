import get_fundamental_data
import get_stock_classification_data
import get_stock_deal_data
import os
import sys
from multiprocessing import Pool
from multiprocessing import Process
parent_path = sys.path[0].split('service')[0]  + '/service/loggings'
if parent_path not in sys.path:
    sys.path.append(parent_path)
import log_processor

logger = log_processor.get_logger(__name__)


def download_tushare_datas():
    logger.info('Run task %s (%s)...' % ('download_tushare_datas', os.getpid()))
    p = Pool()
    p.apply_async(get_fundamental_data.get_fundamental_datas)
    p.apply_async(get_stock_classification_data.get_stock_classification_datas)
    p.apply_async(get_stock_deal_data.get_stock_deal_data)
    p.close()
    p.join()


if __name__ == '__main__':
    process = Process(target=download_tushare_datas)
    process.start()
    process.join()
    print 'test'
