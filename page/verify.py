#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-03 17:31:40
# Filename        : page/verify.py
# Description     : 
from json_handler import JsonRequestHandler
from code.do import get_code

class VerifyHandler(JsonRequestHandler):
    def get(self):
        v = self.get_query_argument('v', '/')
        if not self.need_code():
            self.redirect(v)
            return 

        self.render('verify.html', token = self.token)

    def del_code(self):
        self.acl.del_visits()

    def post(self):
        code = self.get_argument('code', '')
        token = self.get_argument('token', '')
        if code and token and code.lower() == get_code(token).lower():
            self.del_code()
        
        self.redirect(self.get_query_argument('v', '/'))

