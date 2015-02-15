#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-15 21:07:31
# Filename        : admin/api/cache.py
# Description     : 
from .base import ApiAdminHandler, api_admin_authenticated
from lib.wrap import auth_log_save
from public.caches import Cache

class ApiCacheHandler(ApiAdminHandler):
    @api_admin_authenticated
    @auth_log_save
    def delete(self):
        c = Cache()
        c.flush()
        self.result_json['result'] = '缓存已刷新'
        self.write(self.result_json)

        return '缓存已刷新'

