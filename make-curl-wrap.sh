#!/bin/bash

cat curl-wrap-template-pre.txt curl.py curl-wrap-template-post.txt > curl-wrap.sh
chmod +x curl-wrap.sh

