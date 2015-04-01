#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-04 18:48:33
# Filename        : lib/enc.py
# Description     : 
#from uuid import uuid4
from hashlib import md5
from public.data import redis_db
from public.do import made_uuid

def enc_password(password):
    slat = redis_db.get('slat')
    if not slat:
        slat = made_uuid()
        redis_db.set('slat', slat)

    m = md5(password + slat)
    return m.hexdigest()

def get_file_md5(file_path):
    m = md5()
    try:
        fd = open(file_path, 'rb')
        while True:
            t = fd.read(4096)
            if not t:
                break
            m.update(t)

        fd.close()

        return m.hexdigest()


    except:
        return None

