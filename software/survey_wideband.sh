#!/bin/sh
BASEDIR=$(dirname $0)

# use 47.143 as start frequency with 6 MHz interval so that this can double
# as a survey of most of the DTV channels at their center frequencies
python $BASEDIR/rf-survey.py -c cha,chb -d "A:RX1 A:RX2" --f-start 47.143e6 --f-end 863.143e6 --f-interval 6e6 -l 10 -r 10e6 -b 10e6 -g 0 "$@"
