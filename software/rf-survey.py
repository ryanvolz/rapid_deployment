# Perform a survey over a range of frequncies and record data in DigitalRF format using thor

import argparse
import numpy as np
import subprocess

parser = argparse.ArgumentParser(
    description='Run thor.py at a range of frequencies for a given time interval.',
    epilog='Remaining arguments are passed to thor.py.',
)
parser.add_argument(
    '-c', '--channel', dest='chs', action='append',
    help='''Base channel names to use in data directory. The names will have
            the frequency appended as "_{FREQ}MHz" for each interval.
            (default: "ch0")''',
)
parser.add_argument(
    '--f-start', dest='start_freq', default='50e6',
    help='''Starting frequency. (default: %(default)s)''',
)
parser.add_argument(
    '--f-end', dest='end_freq', default='860e6',
    help='''Ending frequency. (default: %(default)s)''',
)
parser.add_argument(
    '--f-interval', dest='interval', default='5e6',
    help='''Frequency step. (default: %(default)s)''',
)
parser.add_argument(
    '-l', '--duration', dest='duration',
    default='10',
    help='''Duration of recording for each interval, in seconds.
            (default: %(default)s)''',
)
parser.add_argument(
    '-e', '--endtime', dest='endtime',
    metavar='', help=argparse.SUPPRESS,
)

op, thor_args = parser.parse_known_args()

if op.chs is None:
    op.chs = ['ch0']
# separate any combined arguments
op.chs = [b.strip() for a in op.chs for b in a.strip().split(',')]

start_freq = eval(op.start_freq)
end_freq = eval(op.end_freq)
interval = eval(op.interval)

for center_freq in np.arange(start_freq, end_freq + interval, interval):
    freq_str = '{0:g}MHz'.format(center_freq/1e6)
    channels = ','.join([ch + '_' + freq_str for ch in op.chs])

    args = [
        'thor.py',
        '-c', channels,
        '-f', str(center_freq),
        '-l', op.duration,
    ]
    args += thor_args

    print(' '.join(args))
    ret = subprocess.call(args)
    # 34304 special case for when boost throws an exception when end time
    # termination happens normally
    if ret != 0 and ret != 34304:
        raise RuntimeError('thor.py exited with non-zero status: {0}'.format(ret))
