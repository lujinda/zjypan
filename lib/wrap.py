#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-15 17:55:12
# Filename        : lib/wrap.py
# Description     : 
import functools
from tornado import web, gen
import time
import json
import urllib

def verify_code(method):
    @functools.wraps(method)
    def wrap(self, *args, **kwargs):
        if self.need_code():
            self.redirect('/verify.py?v=' + self.request.uri)
        else:
            result = method(self, *args, **kwargs)
        
    return wrap


def access_log_save(method):
    @functools.wraps(method)
    @web.asynchronous
    @gen.engine
    def wrap(self, *args, **kwargs):
        yield self.log_db.access.insert(self.access_log)
        result = method(self, *args, **kwargs)
        if not self._finished:
            self.finish()

    return wrap


operation_map = {'download': '下载', 'show': '查看', 'delete': '删除', 'upload': '上传'}

def file_log_save(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        func_name = func.__name__
        _log = {
                'operation': operation_map.get(func_name, '未知'),
                'time': long(time.time()),
                'ip': self._request.client_ip,
                'file_key': self._file_key,
                'type': 'file',
                }
        func(self, *args, **kwargs)
        self._request.log_db.file.insert(_log)
    return wrap

def auth_log_save(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        operation = func(self, *args, **kwargs)
        if not operation:
            return

        _log = {
                'operation': operation,
                'ip': self.client_ip,
                'time': long(time.time()),
                'UA': self.UA,
                }

        self.log_db.operation.insert(_log)

    return wrap

