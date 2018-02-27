"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""

from datetime import datetime
import time
import os
import sys
parent_path = sys.path[0].split('service')[0]  + '/service/tushare'
if parent_path not in sys.path:
    sys.path.append(parent_path)
import download_tushare_datas
from daemon_for_scheduler import Daemon

from apscheduler.schedulers.background import BackgroundScheduler


def tick():
    download_tushare_datas.download_tushare_datas()


class MyDaemon(Daemon):
    def run(self):
        weak_up_scheduler()
        while True:
            time.sleep(1)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)


def weak_up_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', start_date=datetime.now(), hours=24)
    scheduler.start()



