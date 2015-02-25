#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-04-26 15:15:51
# Filename        : task/base.py
# Description     : 
from public.handler import MyRequestHandler
from tornado.web import HTTPError
from public.data import db

class TaskHandler(MyRequestHandler):
    def prepare(self):
        if not self.acl.ip_allow():
            raise HTTPError(403)
        self.result_json = {'error': '', 
                'status_code': 200}

    def send_result(self):
        self.write(self.result_json)

    @property
    def db(self):
        return db

