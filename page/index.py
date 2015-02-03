#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-03 15:19:05
# Filename        : page/index.py
# Description     : 
from .json_handler import JsonRequestHandler
from .do import verify_code

class IndexHandler(JsonRequestHandler):
    @verify_code
    def get(self):
        self.render('up.html')

