#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-12 14:32:57
# Filename        : admin/api/base.py
# Description     : 
from functools import wraps
from tornado.web import HTTPError

from admin.base import AdminHandler
class ApiAdminHandler(AdminHandler):
    def prepare(self):
        self.result_json = {'error': '',
                'status_code': 200, 'result': []}

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        try:
            self.result_json['error'] = kwargs['exc_info'][1].log_message
        except:
            self.result_json['error'] = 'unknown'

        self.result_json['status_code'] = status_code
        self.write(self.result_json)

    def _send_result(self, data, error):
        if error:
            raise HTTPError(500, error)
        elif data:
            self.result_json['result'].append(data)
        else:
            self.write(self.result_json)
            self.finish()

def api_admin_authenticated(method):
    @wraps(method)
    def wrap(self, *args, **kwargs):
        if not self.valid_user():
            raise HTTPError(403)
        result = method(self, *args, **kwargs)

    return wrap

