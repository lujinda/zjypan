#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-22 19:26:04
# Filename        : admin/index.py
# Description     : 
from .base import AdminHandler, valid_authenticated
from lib.info import get_server_info

class AdminIndexHandler(AdminHandler):
    def get(self):
        self.render('index.html', server_info = get_server_info())

