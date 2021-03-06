#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-27 13:39:17
# Filename        : admin/api/base.py
# Description     : 
from functools import wraps
from tornado.web import HTTPError

from admin.base import AdminHandler
from public.handler import ApiHandler
class ApiAdminHandler(ApiHandler, AdminHandler):
    pass

def api_admin_authenticated(method):
    @wraps(method)
    def wrap(self, *args, **kwargs):
        if (not self.valid_user()) and self.UA != 'lujinda app': #  headers中带了相关信息也行
            raise HTTPError(403)
        result = method(self, *args, **kwargs)

    return wrap

