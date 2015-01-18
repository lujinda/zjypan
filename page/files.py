#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-18 13:27:54
# Filename        : page/files.py
# Description     : 
from tornado.web import RequestHandler, asynchronous
import time


class FileHandler(RequestHandler):
    def get(self):
        self.render('file.html')

    @asynchronous
    def post(self):
        files = self.request.files['file']
        for f in files:
            pass
        self.finish()

