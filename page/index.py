#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-08 15:31:44
# Filename        : page/index.py
# Description     : 
from public.handler import MyRequestHandler
from lib.wrap import verify_code, access_log_save

class IndexHandler(MyRequestHandler):
    @access_log_save
    @verify_code
    def get(self):
        self.render('up.html')

