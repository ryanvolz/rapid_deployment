#!/bin/sh
BASEDIR=$(dirname $0)

python $BASEDIR/rf_hop.py -c cha,chb -d "A:RX1 A:RX2" -f 88.3e6,102.7e6,105.5e6,106.3e6,107.7e6 -l 1150,600,600,600,600 --num_cycles 48 -r 1e6 -i 8 -b 10e6 -g 0 "$@"
