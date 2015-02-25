#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-22 19:26:27
# Filename        : admin/log.py
# Description     : 
from .base import AdminHandler
from public.log import operation_log_group, access_log_group

class LogHandler(AdminHandler):
    def get(self, log_type):
        assert log_type in ('access', 'file')
        render_func = getattr(self, 'render_' + log_type)
        render_func()

    def render_file(self):
        self.render('log/log_file.html', operation_list = operation_log_group('file')) # operation_list里面放的是mongo被group后的结果{'_id': 操作, 'count': 记录数}

    def render_access(self):
        self.render('log/log_access.html', status_code_list = access_log_group())

class LogMonitorHandler(AdminHandler):
    def get(self):
        self.render('log/log_monitor.html')


