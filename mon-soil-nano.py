#!/usr/bin/python

# monitoring script to send off sensor data from soild humidity sensor to statsd
# this should be called from crontab loke this: 
# 
# m h  dom mon dow   command
# * * * * * THREESCALE_USER_KEY=your_key_here $HOME/github/abarbanell/rpym/mon-soil-nano.py
#
# this expects the statsd server listed in the /etc/hosts table like this: 
#
# 192.160.100.100 statsd
#
# this version is vor the Arduino Nano(connected as /dev/ttyUSB0) which is
# connecting to only a soil hygrometer sensor with this sketch:
# 
# https://github.com/abarbanell/arduino-sensor/tree/master/soil-echo


import statsd
import serial
import json
import os
import time
import requests
import datetime

# setup
host = os.uname()[1]
# need to find a way to detect the correct USB port device
ser = serial.Serial('/dev/ttyUSB1', 9600)
# we need to wait for the arduino to reset itself before we write..
time.sleep(2)

# send data to get data - it does not matter what we send but 
# character triggers one measurement, so we only send on char

cnt = ser.write('g')

msg = ser.readline()

res = json.loads(msg)
soil = res[u"soil"]

# send data to statsd
c = statsd.StatsClient('statsd', 8125, prefix=host)

c.gauge('sensor.soil', soil)


# send data to limitless-garden
url='http://limitless-garden-9668.herokuapp.com/api/collections/sensor'
querypayload={'user_key': os.getenv('THREESCALE_USER_KEY')};

res[u"host"] = host;
res[u"sensor"] = 'soil';
res[u"timestamp"] = datetime.datetime.utcnow().isoformat();


r = requests.post(url, params=querypayload, json=res)


