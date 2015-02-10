#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-10 19:33:42
# Filename        : public/handler.py
# Description     : 

from tornado.web import RequestHandler
from uuid import uuid4
from lib.acl import ACL
import json

class MyRequestHandler(RequestHandler):
    def initialize(self):
        self.acl = ACL(self.client_ip)

    def write_json(self, data):
        json_data = json.dumps(data)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json_data)

    @property
    def client_ip(self):
        return self.request.remote_ip

    @property
    def UA(self):
        return self.request.headers.get('User-Agent', '')

    @property
    def token(self):
        token = self.get_secure_cookie('token') or ''
        if not token.strip():
            token = uuid4().hex
            self.set_secure_cookie('token', token)

        return token.strip()

    def need_code(self):
        return self.acl.need_code()

    @property
    def access_log(self):
        return {'type': 'access',
                'status_code': self.get_status(),
                'method': self.request.method,
                'client_ip': self.client_ip,
                'path': self.request.uri,
                'cost': self.request.request_time() * 1000,
                'UA': self.UA}

    @property
    def log_db(self):
        return self.application.log_db

