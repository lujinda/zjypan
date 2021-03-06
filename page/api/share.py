#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-15 20:14:08
# Filename        : page/api/share.py
# Description     : 
from public.handler import ApiHandler
from public.data import db_async
from tornado.web import asynchronous
from public.do import get_settings
from lib import cache
import re

class ApiShareHandler(ApiHandler):
    @asynchronous
    def get(self, operation = None):
        """
        返回共享文件列表
        """
        condition = self.get_condition(operation)
        limit, skip = self.made_limit_skip()
        db_async.share.find(condition, {'_id': 0}).sort([('share_time', -1)]).skip(skip).limit(limit).each(self._send_result)

    @classmethod
    def get_condition(cls, operation):
        operation = operation or ('all/all') # 默认是all
        _type, _value = operation.split('/', 1)
        assert _type in ('sort', 'search' , 'all')

        func = getattr(cls, 'list_' + _type)  # 这些函数返回查询条件

        return func(_value)


    @classmethod
    def list_all(self, _value):
        self._title = u'资源文件'
        return {}

    @classmethod
    def list_sort(self, _value):
        self._title = _value
        return {'file_type': _value}

    @classmethod
    def list_search(self, _value):
        self._title = _value + u' 搜索结果'
        _value = re.sub(r'(?P<char>[^\w|\.])', 
                lambda m: '\\' + m.group('char'), _value) # 把除了英语字母下划线还有小数点外的所有字符转义
        return {'file_name': {'$regex': r".*%s.*" % _value}}

    def made_limit_skip(self):
        """
        根据当前页和每页显示的文件数来计算出数据库的limit和skip
        """
        page_limit = self.share_settings['page_limit']
        now_page = int(self.get_argument('page', 1))

        return page_limit, page_limit * (now_page - 1)

    @property
    @cache.cache(expired = 7200)
    def share_settings(self):
        return get_settings('share')

