#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-22 14:51:19
# Filename        : /home/ljd/py/zjypan/public/do.py
# Description     : 
from public.data import db, log_db_sync
from uuid import uuid4
import time

def get_settings(obj):
    return db.settings[obj].find_one() or {}

def save_settings(obj, **settings):
    return db.settings[obj].update({}, settings, True)

def made_uuid():
    return uuid4().hex

def swith_time(long_time):
    return time.strftime('%Y-%m-%d %T', 
            time.localtime(long_time))

