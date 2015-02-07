#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-06 20:00:42
# Filename        : page/index.py
# Description     : 
from .json_handler import JsonRequestHandler
from lib.wrap import verify_code, access_log_save

class IndexHandler(JsonRequestHandler):
    @access_log_save
    @verify_code
    def get(self):
        self.render('up.html')

