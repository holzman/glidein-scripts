#!/bin/bash

wget -q http://169.254.169.254/latest/meta-data/spot/termination-time -O /dev/null

if [ $? -eq 0 ]
then
    killall -TERM glidein_startup.sh
fi
