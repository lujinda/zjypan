#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-15 14:13:31
# Filename        : admin/resources.py
# Description     : 
from .base import AdminHandler, valid_authenticated

class AdminResourcesHandler(AdminHandler):
    @valid_authenticated
    def get(self):
        self.render('resources.html')

