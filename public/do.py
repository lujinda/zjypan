#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-11 20:48:52
# Filename        : public/do.py
# Description     : 
from public.data import db

def get_settings(obj):
    return db.settings[obj].find_one() or {}

