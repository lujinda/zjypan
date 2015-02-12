#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-12 15:25:59
# Filename        : public/do.py
# Description     : 
from public.data import db

def get_settings(obj):
    return db.settings[obj].find_one() or {}

def save_settings(obj, **settings):
    return db.settings[obj].update({}, settings, True)

