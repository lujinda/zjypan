#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-10 15:21:30
# Filename        : lib/info.py
# Description     : 
from public.data import db
import tornado

def get_server_info():
    import time
    import platform
    server_info = {
            'server_time': time.ctime(),
            'os': platform.platform(),
            'python': platform.python_version(),
            'tornado_version': tornado.version,
            }
    return server_info

