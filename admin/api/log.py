#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-16 20:50:58
# Filename        : admin/api/log.py
# Description     : 
from .base import ApiAdminHandler, api_admin_authenticated
from public.log import get_start_stop_time
from tornado.web import asynchronous

class ApiLogHandler(ApiAdminHandler):
    @api_admin_authenticated
    @asynchronous
    def get(self, log_type = None):
        assert log_type in ('file', 'access')
        start = self.get_query_argument('start', None)
        stop = self.get_query_argument('stop', None)
        self._limit = int(self.get_query_argument('limit', 10))
        self._skip = int(self.get_query_argument('offset', 0))
        if start: # 先把日志的时间定好。因为这是所有日志都有的，所以在get就把它处理好，构造时间有空的查询条件
            _start, _stop = get_start_stop_time(start, stop)
            self._condition = [{'time': {'$gte': _start, "$lte": _stop}}]
        else:
            self._start, self._stop = None, None
            self._condition = []

        log_func = getattr(self, 'log_' + log_type, None)
        log_func()

    def log_file(self):
        operation = self.get_query_argument('operation', None)
        if operation:
            self._condition.append({'operation': operation})

        self.log_db['file'].find(self.find_condition, {'_id': 0}).sort([('time', -1)]).skip(self._skip).limit(self._limit).each(self._send_result)

    def log_access(self):
        status_code = int(self.get_query_argument('status_code', 0))
        if status_code:
            self._condition.append({'status_code': status_code})
        self.log_db['access'].find(self.find_condition, {'_id': 0}).sort([('time', -1)]).skip(self._skip).limit(self._limit).each(self._send_result)
    
    @property
    def find_condition(self):
        if self._condition == []:
            return {}
        else: # 如果已经有多个条件了，就加上$and
            return {"$and": self._condition}

    def log_acount(self):
        pass

