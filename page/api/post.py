#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-09 12:34:50
# Filename        : page/api/post.py
# Description     : 
from public.handler import ApiHandler
from public.data import db_async
from tornado.web import asynchronous

class ApiPostHandler(ApiHandler):
    """
    返回特定的通告消息
    """
    @asynchronous
    def get(self):
        limit = int(self.get_query_argument('limit', 1))
        skip = int(self.get_query_argument('skip', 0))
        self.set_header('Cache-Control', 'max-age=600')
        db_async.page.post.find({}, {'_id': 0}).sort([('post_important', -1),('post_time', -1)]).skip(skip).limit(limit).each(self._send_result)

