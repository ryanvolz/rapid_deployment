# Perform a survey over a range of frequncies and record data in DigitalRF format using thor

import argparse
import numpy as np
import subprocess

def evalint(s):
    """Evaluate string to an integer."""
    return int(eval(s, {}, {}))


def evalfloat(s):
    """Evaluate string to a float."""
    return float(eval(s, {}, {}))


class Extend(argparse.Action):
    """Action to split comma-separated arguments and add to a list."""

    def __init__(self, option_strings, dest, type=None, **kwargs):
        if type is not None:
            itemtype = type
        else:
            def itemtype(s):
                return s

        def split_string_and_cast(s):
            return [itemtype(a.strip()) for a in s.strip().split(',')]

        super(Extend, self).__init__(
            option_strings, dest, type=split_string_and_cast, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        cur_list = getattr(namespace, self.dest, [])
        if cur_list is None:
            cur_list = []
        cur_list.extend(values)
        setattr(namespace, self.dest, cur_list)


parser = argparse.ArgumentParser(
    description='Cycle through a list of frequencies and record at each for a time interval.',
    epilog='Remaining arguments are passed to thor.py.',
)
parser.add_argument(
    '-c', '--channel', dest='chs', action=Extend,
    help='''Base channel names to use in data directory. The names will have
            the frequency and cycle appended as "_{FREQ}MHz_{CYCLE}" for each
            interval. (default: "ch0")''',
)
parser.add_argument(
    '-f', '--centerfreq', dest='centerfreqs', action=Extend, type=evalfloat,
    help='''Comma-separated list of center frequencies in Hz.
            (default: 100e6)''',
)
parser.add_argument(
    '-l', '--duration', dest='duration', type=evalint,
    default='15*60*60 - 20',
    help='''Duration of recording for each interval, in seconds.
            (default: %(default)s)''',
)
parser.add_argument(
    '--num_cycles', type=evalint, default=10,
    help='''Number of cycles to record.
            (default: %(default)s)''',
)
parser.add_argument(
    '-e', '--endtime', dest='endtime',
    metavar='', help=argparse.SUPPRESS,
)

op, thor_args = parser.parse_known_args()

if op.chs is None:
    op.chs = ['ch0']

for k in range(op.num_cycles):
    cycle_str = '{0}'.format(k)
    for center_freq in op.centerfreqs:
        freq_str = '{0:g}MHz'.format(center_freq/1e6)
        channels = ','.join(['_'.join([ch, freq_str, cycle_str]) for ch in op.chs])

        args = [
            'thor.py',
            '-c', channels,
            '-f', str(center_freq),
            '-l', str(op.duration),
        ]
        args += thor_args

        print(' '.join(args))
        ret = subprocess.call(args)
        # 34304 special case for when boost throws an exception when end time
        # termination happens normally
        if ret != 0 and ret != 34304:
            raise RuntimeError('thor.py exited with non-zero status: {0}'.format(ret))
