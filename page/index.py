#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-25 14:25:28
# Filename        : page/index.py
# Description     : 
from tornado.web import RequestHandler

class IndexHandler(RequestHandler):
    def get(self):
        self.render('up.html')

