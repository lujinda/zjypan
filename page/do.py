#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-18 21:29:33
# Filename        : page/do.py
# Description     : 
import time
import string
import random
from public.data import db

def get_upload_time():
    return long(time.time())

def get_expired_time(days = 3):
    return long(time.time() + 24 * 60 * 60 * 3)

def get_file(file_key):
    return db.files.find_one({'key': file_key})

def made_file_key():
    localtime = time.localtime()
    while True:
        file_key = "%2d%s%s%s"%(localtime.tm_mday , localtime.tm_wday + 1 , \
                random.choice(string.ascii_letters) , random.choice(string.ascii_letters))
        if not get_file(file_key):
            break

    return file_key

