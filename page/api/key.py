#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-16 13:22:49
# Filename      : key.py
# Description   : 
from public.handler import ApiHandler
from tornado.web import HTTPError
from public.data import redis_db
from page.do import FileManager

def get_set_key(openid):
    """根据openid生成"""
    return "oauth:key:" + openid

def append_key_to_set(openid, file_key):
    """如果当前有qq登录，则把key加入到qq号当中去"""
    redis_db.sadd(get_set_key(openid), file_key)

def remove_key_from_set(openid, file_key):
    redis_db.srem(get_set_key(openid), file_key)

class KeyManagerHandler(ApiHandler):
    def init_data(self):
        super(KeyManagerHandler, self).init_data()
        self.openid = self.session.get('openid', None)
        if not (self.openid):
            self.result_json['error'] = '没有登录账号'

    def get(self, file_key = None):
        """列出所有"""
        if not self.openid:
            return

        if file_key:
            file_manager = FileManager(file_key)
            self.result_json['result'] = list(file_manager.get_file_list())
        else:
            key_list = list(redis_db.smembers(get_set_key(self.openid)))
            self.result_json['result'] = key_list

    def post(self, file_key):
        """添加一个key"""
        if not self.openid:
            return
        append_key_to_set(self.openid, file_key)

    def delete(self, file_key):
        """添加一个key"""
        if not self.openid:
            return
        remove_key_from_set(self.openid, file_key)

