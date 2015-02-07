#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-06 20:40:38
# Filename        : lib/wrap.py
# Description     : 
import functools
from tornado import web, gen

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
        yield self.application.log_db.access.insert(self.access_log)
        method(self, *args, **kwargs)

    return wrap

