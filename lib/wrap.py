#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-14 15:40:57
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
            if self.referer.split('/')[-1] == 'manage.py': # 如果是从manage.py页面过来的话，需要验证码不重定向，而是返回消息
                self.write({'error': '请不要上传这么频繁'})
            else:
                self.redirect('/verify.py?v=' + self.request.uri)
        else:
            result = method(self, *args, **kwargs)
        
    return wrap

def allow_add_share_num(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if not self.acl.allow_add_share_num(self._share_id):
            self.result_json['error'] = '您已评论过该文件了'
            self.send_result_json()
            return
        else:
            self.acl.add_share_num_register(self._share_id)
            return func(self, *args, **kwargs)

    return wrap

def allow_feedback(method):
    @functools.wraps(method)
    def wrap(self, *args, **kwargs):
        if self.acl.allow_feedback():
            self.acl.add_feedback_register()
            return method(self, *args, **kwargs)
        else:
            self.result_json['error'] = 1
            self.result_json['result'] = '请不要这么频繁提交反馈，谢谢您对我们的关注'
            self.send_result_json()

    return wrap

def access_log_save(method):
    @functools.wraps(method)
    @web.asynchronous
    @gen.engine
    def wrap(self, *args, **kwargs):
        yield self.save_access_log()
        result = method(self, *args, **kwargs)
        if not self._finished:
            self.finish()

    return wrap


operation_map = {'download': '下载', 'show': '查看', 'delete': '删除', 'upload': '上传', 'expired': '过期', 
        'speed_upload': '极速上传', 'share': '共享', 'unshare': '取消共享'}

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

