#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-11 16:42:02
# Filename        : admin/api/operation.py
# Description     : 
from .base import ApiAdminHandler, api_admin_authenticated
from tornado.web import asynchronous
from tornado import gen

class ApiOperationHandler(ApiAdminHandler):
    @api_admin_authenticated
    @asynchronous
    def get(self):
        limit = int(self.get_query_argument('limit', 10))
        skip = int(self.get_query_argument('offset', 0))
        self.log_db.operation.find({}, {'_id': 0}).sort([('time', -1)]).skip(skip).limit(limit).each(self._send_result)

