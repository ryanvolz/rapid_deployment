#!/bin/sh
BASEDIR=$(dirname $0)

python $BASEDIR/rf-survey.py -c cha,chb -d "A:RX1 A:RX2" --f-start 87.5e6 --f-end 107.9e6 --f-interval 200e3 -l 60 -r 1e6 -i 4 -b 10e6 -g 0 "$@"
