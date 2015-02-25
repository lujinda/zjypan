#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-25 12:57:24
# Filename        : /home/ljd/py/zjypan/page/index.py
# Description     : 
from public.handler import MyRequestHandler
from lib.wrap import verify_code, access_log_save
from lib import cache

class IndexHandler(MyRequestHandler):
    @access_log_save
    @verify_code
#    @cache.page()
    def get(self):
        self.render('up.html')

