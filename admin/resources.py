#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-22 19:28:10
# Filename        : admin/resources.py
# Description     : 
from .base import AdminHandler

class AdminResourcesHandler(AdminHandler):
    def get(self):
        self.render('resources.html')

