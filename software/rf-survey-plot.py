from argparse import ArgumentParser
import os
import digital_rf as drf
import datetime

plots = [
    dict(name='specgram', type='specgram', use_log=True, bins='1024'),
    dict(name='spectrum', type='spectrum', use_log=True, bins='1024'),
    dict(name='voltage', type='voltage'),
    dict(name='phase', type='phase', use_log=True, bins='128'),
    dict(name='iq', type='iq'),
    dict(name='iq_bits', type='iq', use_log=True),
    dict(name='histogram', type='histogram', use_log=True, bins='128'),
]

parser = ArgumentParser()
parser.add_argument('dir')
parser.add_argument('-t', dest='plot_time', default='1000', help='Time span to plot (milliseconds)')
parser.add_argument('-s', dest='save_dir', default='.')
args = parser.parse_args()

chans = sorted(os.listdir(args.dir))

#plot_cmd = '~/midasmicro/digital_rf/drf_plot.py'
plot_cmd = 'drf_plot.py'
i = 0
for chan in chans:
    chan_string = chan + ':0'
    mdf = drf.DigitalMetadataReader(args.dir + chan + '/metadata')

    mdbounds = mdf.get_bounds()
    print mdbounds

    #need to get sample rate to interpret bounds
    latest = mdf.read_latest()
    latest_md = latest[latest.keys()[0]]
    sfreq = latest_md['sample_rate']

    mdt = mdf.read(mdbounds[0],mdbounds[1])
    times = mdt.keys()

    for time in times:
        print "time: " + str(time)
        start_time = datetime.datetime.utcfromtimestamp(time/sfreq)
        start_time_string = start_time.isoformat()
        md = mdt[time]
        cfreq = int(md['center_frequencies'].ravel()[0])
        print "cfreq: " + str(cfreq)
        print "sfreq: " + str(sfreq)
        num_samples = int(sfreq*int(args.plot_time)/1000)
        sample_range = '0:{:d}'.format(num_samples)
        for opts in plots:
            command_line = ' '.join([plot_cmd, '-i', args.dir, '-p', opts['type'], '-r', \
sample_range, '-c', chan_string, '-a', start_time_string])

            if 'use_log' in opts and opts['use_log']:
                command_line += ' -l'
            if 'dynamic_range' in opts:
                command_line += ' -z ' + opts['dynamic_range']
            if 'num_bins' in opts:
                command_line += ' -b ' + opts['num_bins']
            if args.save_dir != "":
                fname = '_'.join([opts['name'],chan,str(cfreq)])
                command_line += ' -s ' + os.path.join(args.save_dir, fname + '.png')
            print command_line
            #rtn = 0
            #i += 1
            #if i > 5:
            #    quit()
            rtn = os.system(command_line)
            if rtn:
                raise RuntimeError('drf-plot exited with non-zero status')
