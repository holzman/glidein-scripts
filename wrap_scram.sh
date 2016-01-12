#!/bin/bash

CURLPATH=/tmp/curlpath

scram $1 $2

if [ x$1 == "xruntime" ]; then
    if [ x$2 == "x-csh" ]; then
	echo setenv PATH ${CURLPATH}:\$\{PATH\}
    fi
    if [ x$2 == "x-sh" ]; then
	echo export PATH=${CURLPATH}:\$\{PATH\}
    fi

fi


