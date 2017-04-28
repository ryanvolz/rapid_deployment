# Perform a survey over a range of frequncies and record data in DigitalRF format using thor
# 2017 Gregory Allan

import time
import datetime
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('dir')
parser.add_argument('-r', dest='sample_rate', default='10e6')
parser.add_argument('-c', dest='channels', default='cha,chb')
parser.add_argument('-d', dest='devices', default="\"A:RX1 A:RX2\"")
parser.add_argument('--f-start', dest='start_freq', default='50e6')
parser.add_argument('--f-end', dest='end_freq', default='860e6')
parser.add_argument('-i', dest='interval', default='5e6')
parser.add_argument('-g', dest='gain', default='0')

op = parser.parse_args()

thorcommand = "thor.py"

center_freq = eval(op.start_freq)
interval = eval(op.interval)
while center_freq <= eval(op.end_freq):
    now = datetime.datetime.utcnow()
    now = now.replace(microsecond=0)
    starttime = (now + datetime.timedelta(seconds=10)).isoformat() + 'Z'
    duration = 10
    freq_str = '{0:0.0f}MHz'.format(center_freq/1e6)
    channels = ','.join([ch + '_' + freq_str for ch in channels.split(',')])
    bash_command = ' '.join([thorcommand, '-c', channels, '-d', op.devices, '-f', str(center_freq), '-g', op.gain, '-r', op.sample_rate, '-s', starttime, '-l', str(duration), '-b', '10e6', '-a', '"peak=0.0625"', op.dir])
    print bash_command
    ret = os.system(bash_command)
    # 34304 special case for when boost throws an exception when end time
    # termination happens normally
    if ret != 0 and ret != 34304:
        raise RuntimeError('thor.py exited with non-zero status: {0}'.format(ret))
    center_freq += interval
