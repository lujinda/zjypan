#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-25 20:33:26
# Filename        : t.py
# Description     : 

import os

for root, dirname, filesname in os.walk('.'):
    for filename in filesname:
        if filename[0] == '.':
            continue
        print os.path.join(root, filename)[2:]


