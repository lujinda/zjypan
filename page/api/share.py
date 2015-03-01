#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-28 18:46:48
# Filename        : page/api/share.py
# Description     : 
from public.handler import ApiHandler
from public.data import db_async
from public.do import get_settings
from tornado.web import asynchronous
from lib import cache

class ApiShareHandler(ApiHandler):
    @asynchronous
    def get(self):
        """
        返回共享文件列表
        """
        self.list_all()


    def list_all(self):
        limit, skip = self.made_limit_skip()
        db_async.share.find({}, {'_id': 0}).sort([('share_time', -1)]).skip(skip).limit(limit).each(self._send_result)

    def made_limit_skip(self):
        """
        根据当前页和每页显示的文件数来计算出数据库的limit和skip
        """
        page_limit = self.settings.get('page_limit', 16)
        now_page = int(self.get_argument('page', 1))
        print now_page

        return page_limit, page_limit * (now_page - 1)

    @property
    @cache.cache(expired = 7200)
    def settings(self):
        return get_settings('share')


