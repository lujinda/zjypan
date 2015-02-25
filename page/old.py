#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-24 15:57:50
# Filename        : page/old.py
# Description     : 
from page import IndexHandler
from lib.wrap import verify_code, access_log_save
from lib import cache

class OldIndexHandler(IndexHandler):
    @access_log_save
    @verify_code
    @cache.page()
    def get(self):
        self.render('old_up.html')

