#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-27 13:24:17
# Filename        : public/data.py
# Description     : 

import pymongo
import os

db = pymongo.Connection().zjypan

def del_local_file(file_path):
    dir_name = os.path.dirname(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        os.removedirs(dir_name)

