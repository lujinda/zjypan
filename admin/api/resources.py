#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-06 16:40:06
# Filename        : /home/ljd/py/zjypan/admin/api/resources.py
# Description     : 
from .base import ApiAdminHandler, api_admin_authenticated
from public.log import get_range_log
from datetime import date, timedelta
from page.do import get_save_total_num, get_up_total_num
from lib import cache

class ApiResourcesHandler(ApiAdminHandler):
    """
    资源统计
    """
    @api_admin_authenticated
    def get(self):
        self._condition = {'operation': '上传'}
        today_num = self.get_today_num()
        yesterday_num = self.get_yesterday_num()
        up_total_num = self.get_up_total_num()
        save_total_num = self.get_save_total_num()
        self.result_json['result'] = dict(today_num = today_num, yesterday_num = yesterday_num,
            up_total_num = up_total_num, save_total_num = save_total_num)
        self.write(self.result_json)

    def get_today_num(self):
        return get_range_log(date.today().timetuple(), 
                condition = self._condition).count()
        
    @cache.cache(expired = 86400000)
    def get_yesterday_num(self):
        return get_range_log((date.today() - timedelta(days = 1)).timetuple(), 
                condition = self._condition).count()

    def get_save_total_num(self):
        return get_save_total_num()

    def get_up_total_num(self):
        return get_up_total_num()

