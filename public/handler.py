#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-15 10:18:28
# Filename        : public/handler.py
# Description     : 

from tornado.web import RequestHandler, asynchronous
from tornado.websocket import WebSocketHandler
from uuid import uuid4
from lib.acl import ACL
from copy import deepcopy
import json
import time
from lib.wrap import access_log_save, auth_log_save
try:
    from tornado.curl_httpclient import AsyncHTTPClient
except ImportError:
    from tornado.simple_httpclient import AsyncHTTPClient

from tornado.httpclient import HTTPRequest
from lib.session import Session

class MyRequestHandler(RequestHandler):
    def initialize(self):
        self.acl = ACL(self.client_ip)
        self.session = Session(self.application.session_manager, self)
        self.init_data()

    def init_data(self):
        """
        另做一个勾子用于类被实例化时调用
        """
        pass

    def send_result_json(self):
        """
        只要类属性中有result_json，并且为字典就可以以json方式发送
        """
        if self._finished:
            return
        result_json = self.__dict__.get('result_json')
        assert isinstance(result_json, dict) 
        self.write(result_json)

    def write_json(self, data):
        json_data = json.dumps(data)
        self.set_header('Content-Type', 'text/html; charset=UTF-8') # 为了兼容各种浏览器。面向管理员的不调write_json方法
        self.write(json_data)

    @property
    def client_ip(self):
        return self.request.remote_ip

    @property
    def UA(self):
        return self.request.headers.get('User-Agent', '')

    def full_host(self):
        return '%s://%s' %(self.request.protocol, self.request.host)

    @property
    def token(self):
        token = self.get_secure_cookie('token') or ''
        if not token.strip():
            token = uuid4().hex
            self.set_secure_cookie('token', token)

        return token.strip()

    def need_code(self):
        return self.acl.need_code()
    
    def prepare(self):
        """
        判断是否服务器进入维护状态了
        """
        stop, stop_info = self.acl.need_stop()
        if stop and self.session.get('uid') != 0: # 如果已经登录了后台管理员，则维护状态不会起效果
            self.render('stop.html', stop_info = stop_info)
            self.save_access_log() # 在同步的情况下，也把访问日志插入

    def save_access_log(self):
        return self.log_db.access.insert(self.access_log)

    @property
    def access_log(self):
        return {'type': 'access',
                'status_code': self.get_status(),
                'method': self.request.method,
                'client_ip': self.client_ip,
                'path': self.request.uri,
                'time': long(time.time()),
                'cost': round(self.request.request_time() * 1000, 2),
                'UA': self.UA}

    def flush(self, *args, **kwargs):
        """
        重构flush，为了获取缓存区数据
        """
        self._buffer = deepcopy(self._write_buffer)
        super(MyRequestHandler, self).flush(*args, **kwargs)

    @property
    def log_db(self):
        return self.application.log_db

    @property
    def referer(self):
        return self.request.headers.get('Referer', '')

class ApiHandler(MyRequestHandler):
    def init_data(self):
        self.result_json = {'error': '',
                 'result': []}
        self.__is_send_result = False # 标记是否执行了_send_result

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        try:
            self.result_json['error'] = kwargs['exc_info'][1].log_message
        except:
            self.result_json['error'] = 'unknown'

        self.result_json['status_code'] = status_code
        self.write(self.result_json)

    def _send_result(self, data=None, error=None):
        if error:
            raise HTTPError(500, error)
        elif data:
            self.result_json['result'].append(data)
        else:
            self.write(self.result_json)
            self.__is_send_result = True
            self.finish()

    def send_result_json(self, *args, **kwargs):
        return self._send_result(*args, **kwargs)

    @asynchronous
    def async_request(self, url, callback, method = None, headers = None, body = None):
        headers = headers or {}
        method = method or "GET"
        http_client = AsyncHTTPClient()
        http_request = HTTPRequest(url = url, method = method, headers = headers, body = body, validate_cert = False)
        http_client.fetch(http_request, callback)

    def finish(self, *args, **kwargs):
        if (not self.__is_send_result) and self._status_code in (200, 304):
            self.write(self.result_json)
        super(ApiHandler, self).finish(*args, **kwargs)

from tornado.web import HTTPError

class DefaultHandler(MyRequestHandler):
    """处理404"""
    def prepare(self):
        self.set_status(404)
        self.write('The server may be lost')
        self.finish()

    @access_log_save
    def on_finish(self):
        raise HTTPError(404)

class MonitorHandler(WebSocketHandler):
    """
    用来处理websocket
    """
    @auth_log_save
    def open(self):
        self.application.monitors_manager.register(self.callback)
        return '查看实时监控'

    def on_close(self):
        self.application.monitors_manager.unregister(self.callback)

    def on_message(self, message):
        pass

    def callback(self, message):
        self.write_message(message)

    @property
    def client_ip(self):
        return self.request.remote_ip

    @property
    def UA(self):
        return self.request.headers.get('User-Agent', '')

    @property
    def log_db(self):
        return self.application.log_db


