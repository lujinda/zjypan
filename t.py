#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-13 17:48:56
# Filename        : t.py
# Description     : 

from public.data import settings_db
import json

print settings_db.hset('global', 'stop', True)
(settings_db.hgetall('global'))

