#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-22 19:27:50
# Filename        : admin/logout.py
# Description     : 
from .base import BaseHandler

class LogoutHandler(BaseHandler):
    def get(self):
        self.session.logout()
        self.redirect('/tuxpy')

    def prepare(self):
        """
        重勾它，因为BaseHandler的这个方法都做了用户认证，而登录的这个不需要的
        """
        pass

