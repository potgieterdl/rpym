#!/usr/bin/python

# monitoring script to send off some system stats to statsd.
# this should be called from crontab loke this: 
# 
# m h  dom mon dow   command
# * * * * * $HOME/github/abarbanell/rpym/mon.py
#
# this expects the statsd server listed in the /etc/hosts table like this: 
#
# 192.160.100.100 statsd
#

from datetime import datetime
import statsd
import os
import psutil
import time
import apscheduler
import logging

logging.basicConfig()

from apscheduler.schedulers.blocking import BlockingScheduler

started = False

def tick():
    global started
    if started is False:
        print('Started successfuly : %s' % datetime.now()) 
        started = True

    # get data
    host = os.uname()[1]
    rasp = ('armv' in os.uname()[4])
    
    cpu = psutil.cpu_percent(interval=1)
    if rasp:
        f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
        l = f.readline()
        temp = 1.0 * float(l)/1000
    usage = psutil.disk_usage("/")
    mem = psutil.virtual_memory()

    # send data
    c = statsd.StatsClient('statsd', 8125, prefix=host)

    c.incr('heartbeat')
    c.gauge('cpu.percent', cpu)

    if rasp:
        c.gauge('cpu.temp', temp)

    c.gauge('disk.root.total', usage.total)
    c.gauge('disk.root.used', usage.used)
    c.gauge('disk.root.free', usage.free)
    c.gauge('disk.root.percent', usage.percent)
    c.gauge('mem.total', mem.total)
    c.gauge('mem.free', mem.free)
    c.gauge('mem.used', mem.used)
    c.gauge('mem.percent', (mem.used/float(mem.total)*100))
    
if __name__ == '__main__':
    print('Starting statsd agent : %s' % datetime.now())
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

