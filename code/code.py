#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-03 17:29:06
# Filename        : code/code.py
# Description     : 
from tornado.web import RequestHandler
from .do import get_image_bin

class CodeHandler(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'image/jpeg')
        token = self.get_query_argument('token', '')
        image_bin = get_image_bin(token)
        self.write(image_bin)
