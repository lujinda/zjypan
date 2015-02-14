#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-14 16:41:07
# Filename        : lib/enc_password.py
# Description     : 
#from uuid import uuid4
from hashlib import md5
from public.data import redis_db

def enc_password(password):
    slat = redis_db.get('slat')
    if not slat:
        slat = '90a4acfaaaca4623be132ed9dca25b35'
        redis_db.set('slat', slat)

    m = md5(password + slat)
    return m.hexdigest()

