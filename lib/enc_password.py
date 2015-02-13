#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-12 16:43:26
# Filename        : lib/enc_password.py
# Description     : 
from uuid import uuid4
from hashlib import md5
from public.data import redis_db

def enc_password(password):
    slat = redis_db.get('slat')
    if not slat:
        slat = uuid4().hex
        redis_db.set('slat', slat)

    m = md5(password + slat)
    return m.hexdigest()

