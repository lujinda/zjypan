#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-10 20:44:24
# Filename        : admin/logout.py
# Description     : 
from .base import BaseHandler

class LogoutHandler(BaseHandler):
    def get(self):
        self.session.logout()
        self.redirect('/tuxpy')

