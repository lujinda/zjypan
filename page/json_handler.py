#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-03 11:49:19
# Filename        : page/json_handler.py
# Description     : 

from tornado.web import RequestHandler
import json

class JsonRequestHandler(RequestHandler):
    def write_json(self, data):
        json_data = json.dumps(data)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json_data)

    @property
    def client_ip(self):
        return self.request.remote_ip

