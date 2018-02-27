#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, re, time, base64, hashlib, logging,glob,datetime

import markdown2

from transwarp.web import get, post, ctx, view, interceptor, seeother, notfound

from apis import api, Page, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
from models import User, Task, TaskRunningLog
from config import configs
from service.tushare.get_stock_deal_data import get_stock_deal_data
from service.tushare.get_stock_deal_data import get_stock_hist_data_multithreading
from service.tushare.get_fundamental_data import get_fundamental_datas_history
from service.tushare.get_fundamental_data import get_fundamental_datas_now
from service.tushare.get_stock_classification_data import get_stock_classification_datas
from apscheduler.schedulers.background import BackgroundScheduler
from service.assurance.get_assurance_data import get_assurance_data
from service.utils.tushare_data_util import upload_daily_files,zip_daily_dir_and_delete

import sys
import threading
#parent_path = sys.path[0].split('service')[0] + '/service/news'
#if parent_path not in sys.path:
#    sys.path.append(parent_path)

#from news.spiders.china_spider import ChinaSpider
#from news.spiders.stockstar_spider import StockstarSpider
#from scrapy.crawler import CrawlerProcess


_COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret


def _get_page_index():
    page_index = 1
    try:
        page_index = int(ctx.request.get('page', '1'))
    except ValueError:
        pass
    return page_index


def make_signed_cookie(id, password, max_age):
    # build cookie string by: id-expires-md5
    expires = str(int(time.time() + (max_age or 86400)))
    L = [id, expires, hashlib.md5('%s-%s-%s-%s' % (id, password, expires, _COOKIE_KEY)).hexdigest()]
    return '-'.join(L)


def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        id, expires, md5 = L
        if int(expires) < time.time():
            return None
        user = User.get(id)
        if user is None:
            return None
        if md5 != hashlib.md5('%s-%s-%s-%s' % (id, user.password, expires, _COOKIE_KEY)).hexdigest():
            return None
        return user
    except:
        return None


def check_admin():
    user = ctx.request.user
    if user and user.admin:
        return
    raise APIPermissionError('No permission.')


@interceptor('/')
def user_interceptor(next):
    logging.info('try to bind user from session cookie...')
    user = None
    cookie = ctx.request.cookies.get(_COOKIE_NAME)
    if cookie:
        logging.info('parse session cookie...')
        user = parse_signed_cookie(cookie)
        if user:
            logging.info('bind user <%s> to session...' % user.email)
    ctx.request.user = user
    return next()


@interceptor('/manage/')
def manage_interceptor(next):
    user = ctx.request.user
    if user and user.admin:
        return next()
    raise seeother('/signin')


@view('signin.html')
@get('/')
def index():
    return dict(user=ctx.request.user)


@view('task_list.html')
@get('/task_list')
def log_list():
    total = Task.count_all()
    page = Page(total, _get_page_index())
    tasks = Task.find_by('order by updated_at desc limit ?,?', page.offset, page.limit)

    return dict(tasks=tasks, page=page, user=ctx.request.user)


@view('task_submit.html')
@get('/task_subimt')
def task_subimt():
    return dict(user=ctx.request.user)


@view('signin.html')
@get('/signin')
def signin():
    return dict()


@get('/signout')
def signout():
    ctx.response.delete_cookie(_COOKIE_NAME)
    raise seeother('/')


@api
@post('/api/authenticate')
def authenticate():
    i = ctx.request.input(remember='')
    email = i.email.strip().lower()
    password = i.password
    remember = i.remember
    user = User.find_first('where email=?', email)
    if user is None:
        raise APIError('auth:failed', 'email', 'Invalid email.')
    elif user.password != password:
        raise APIError('auth:failed', 'password', 'Invalid password.')
    # make session cookie:
    max_age = 604800 if remember == 'true' else None
    cookie = make_signed_cookie(user.id, user.password, max_age)
    ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)
    user.password = '******'
    return user

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')


@api
@post('/api/users')
def register_user():
    i = ctx.request.input(name='', email='', password='')
    name = i.name.strip()
    email = i.email.strip().lower()
    password = i.password
    if not name:
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_MD5.match(password):
        raise APIValueError('password')
    user = User.find_first('where email=?', email)
    if user:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    user = User(name=name, email=email, password=password, image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email).hexdigest())
    user.insert()
    # make session cookie:
    cookie = make_signed_cookie(user.id, user.password, None)
    ctx.response.set_cookie(_COOKIE_NAME, cookie)
    return user


@api
@get('/api/task_list')
def api_get_task_list():
    total = Task.count_all()
    page = Page(total, _get_page_index())
    tasks = Task.find_by('order by updated_at desc limit ?,?', page.offset, page.limit)
    return dict(tasks=tasks, page=page, user=ctx.request.user)



@view('register.html')
@get('/register')
def register():
    return dict()

@view('test.html')
@get('/test')
def test():
    return dict()


@get('/manage/')
def manage_index():
    raise seeother('/task_list')


@view('manage_comment_list.html')
@get('/manage/comments')
def manage_comments():
    return dict(page_index=_get_page_index(), user=ctx.request.user)


@view('manage_user_list.html')
@get('/manage/users')
def manage_users():
    return dict(page_index=_get_page_index(), user=ctx.request.user)

@api
@get('/api/users')
def api_get_users():
    total = User.count_all()
    page = Page(total, _get_page_index())
    users = User.find_by('order by created_at desc limit ?,?', page.offset, page.limit)
    for u in users:
        u.password = '******'
    return dict(users=users, page=page)

@api
@get('/api/task_logs/:task_name')
def api_task_logs(task_name):
    total = TaskRunningLog.count_all()
    page = Page(total, _get_page_index(), page_size=50)
    task_logs = TaskRunningLog.find_by('where task_id = ? order by updated_at desc limit ?,?', task_name, page.offset, page.limit)
    return task_logs

@api
@get('/api/get_fundamental_datas_history')
def api_get_fundamental_datas_history():
    uid = ctx.request.user.id
    task = Task(user_id=uid, task_status='R', task_name='fundamental_datas_history_job', description='tushare基本面数据')
    task.insert()
    get_fundamental_datas_history()
    task = Task(user_id=uid, task_status='C', task_name='fundamental_datas_history_job', description='tushare基本面数据', end_time=time.time(), id=task.id)
    task.update()

    return dict(result='OK')
@api
@get('/api/get_fundamental_datas_now')
def api_get_fundamental_datas_now():
    uid = ctx.request.user.id
    task = Task(user_id=uid, task_status='R', task_name='fundamental_datas_now_job', description='tushare基本面数据')
    task.insert()
    get_fundamental_datas_now()
    task = Task(user_id=uid, task_status='C', task_name='fundamental_datas_now_job', description='tushare基本面数据', end_time=time.time(), id=task.id)
    task.update()

    return dict(result='OK')

@api
@get('/api/get_stock_classification_datas')
def api_get_stock_classification_datas():
    uid = ctx.request.user.id
    task = Task(user_id=uid, task_status='R', task_name='stock_classification_datas_job', description='tushare股票分类数据')
    task.insert()
    get_stock_classification_datas()
    task = Task(user_id=uid, task_status='C', task_name='stock_classification_datas_job', description='tushare股票分类数据', end_time=time.time(), id=task.id)
    task.update()
    return dict(result='OK')


@api
@get('/api/get_stock_deal_data')
def api_get_stock_deal_data():
    uid = ctx.request.user.id
    task = Task(user_id=uid, task_status='R', task_name='stock_deal_data_job', description='tushare股票的交易行情数据')
    task.insert()
    get_stock_deal_data()
    task = Task(user_id=uid, task_status='C', task_name='stock_deal_data_job', description='tushare股票的交易行情数据', end_time=time.time(), id=task.id)
    task.update()
    return dict(result='OK')

@api
@get('/api/get_assurance_data')
def api_get_assurance_data():
    uid = ctx.request.user.id
    task = Task(user_id=uid, task_status='R', task_name='get_assurance_data_job', description='企业担保数据')
    task.insert()
    get_assurance_data()
    task = Task(user_id=uid, task_status='C', task_name='get_assurance_data_job', description='企业担保数据',end_time=time.time(), id=task.id)
    task.update()
    return dict(result='OK')



@api
@get('/api/get_stock_hist_data_multithreading')
def api_stock_hist_data_multithreading():
    uid = ctx.request.user.id
    print uid
    get_stock_hist_data_multithreading()
    return dict(result='OK')



@api
@get('/api/scheduler_start')
def api_scheduler_start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_stock_deal_data, 'cron', hour=2, id='stock_deal_data_job')
    scheduler.add_job(get_assurance_data, 'cron', hour=2, id='get_assurance_data_job')
    scheduler.start()
    return dict(result='OK')


@api
@get('/api/news_scheduler_start')
def api_news_scheduler_start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(api_get_finance_news_data, 'cron', day_of_week='0-6', hour=0, minute=0,second=0, id='get_finance_news_data_job')
    scheduler.start()
    return dict(result='OK')

@api
@get('/api/get_finance_news_data')
def api_get_finance_news_data():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y%m%d')
    rootPath=sys.path[0].split('service')[0] + '/service/news'
    if not os.path.isdir(rootPath+'/files/'+yesterday):
        os.mkdir(rootPath+'/files/'+yesterday)

    executeSpiderMultiThreading()

    outputFileName=rootPath+'/files/'+yesterday+'.txt'
    mergeFiles(rootPath+'/files/'+yesterday,outputFileName)
    zip_daily_dir_and_delete()
    upload_daily_files()
    return dict(result='OK')

def mergeFiles(inputFolder,outputFileName):
    logging.info('合并中。。。')
    outputFile = open(outputFileName, "a")
    for txtFile in glob.glob(os.path.join(inputFolder, "*.txt")):
        print txtFile
        inputFile = open(txtFile, "rb")
        for line in inputFile:
            outputFile.write(line)
    logging.info('合并完成')
    return

def executeSpiderMultiThreading():
    # spiderList=(
    #     'zhonggong','beijiaosuo','jinghua','stocktimes','xiaoxiangcb','dagongguoji',
    # )
    # spiderList1 = (
    #              'juchaozixun',
    #          )
    spiderList1=(
        '10jqka', '163', 'bjd', 'bjx', 'caijing', 'caixin', 'cbtnet', 'ccstock','beijiaosuo','jinghua','stocktimes','xiaoxiangcb',
    )
    # spiderList2 = (
    #      'ce','changjiangtimes','china', 'chinabond', 'chinadaily', 'chinafund', 'chinanews','chinatimes', 'cnfol','cngold','cnr',
    #  )
    # spiderList3 = (
    #     'cnstock','cnwest','cqcb', 'cs','ctafund', 'dayoo','eastday', 'eastmoney','eeo', 'ftchinese', 'funxun', 'gmw', 'hexun', 'hongzhoukan',
    # )
    # spiderList4 = (
    #     'huanqiu', 'ibtimes','ifeng','jf', 'jrj', 'lnd','morningpost', 'naffmi', 'nbd', 'p5w','qhrb','qingdaonews','qq','shclearing','sina','sohu'
    # )
    # spiderList5 = (
    #     'southcn','stockstar','sxdsb','sznews','thepaper','tianjinwe','timeweekly','topcj','wabei','wallstreet','xdkb','xinmin','xkb','yicai','ynet','zj'
    # )
    threads = []
    t1 = threading.Thread(target=executeSpider, args=(spiderList1))
    threads.append(t1)
    # t2 = threading.Thread(target=executeSpider, args=(spiderList2))
    # threads.append(t2)
    # t3 = threading.Thread(target=executeSpider, args=(spiderList3))
    # threads.append(t3)
    # t4 = threading.Thread(target=executeSpider, args=(spiderList4))
    # threads.append(t4)
    # t5 = threading.Thread(target=executeSpider, args=(spiderList5))
    # threads.append(t5)
    for t in threads:
        t.setDaemon(True)
        t.start()
        t.join()

def executeSpider(*spiders):
    rootPath = sys.path[0].split('service')[0] + '/service/news'
    for spider in spiders:
        print spider
        os.system('cd ' + rootPath + ' && scrapy crawl '+spider)




@view('stock.html')
@get('/stock')
def stock_list():
    return dict(user=ctx.request.user)
