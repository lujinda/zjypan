#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-10 20:45:31
# Filename        : admin/index.py
# Description     : 
from .base import AdminHandler
from lib.info import get_server_info
from tornado.web import authenticated

class AdminIndexHandler(AdminHandler):
    @authenticated
    def get(self):
        self.render('admin/index.html', server_info = get_server_info())

