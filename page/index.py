#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-18 21:42:50
# Filename        : page/index.py
# Description     : 
from tornado.web import RequestHandler

class IndexHandler(RequestHandler):
    def get(self):
        self.redirect('/up.py')

