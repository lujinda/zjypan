#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-04-13 19:40:35
# Filename      : index.py
# Description   : 
from .base import GroupBaseHandler, group_is_enabled, group_change_status, valid_key_authenticated
from lib.wrap import access_log_save

class GroupIndexHandler(GroupBaseHandler):
    @access_log_save
    @valid_key_authenticated
    def get(self):
        status = self.get_query_argument('status', None)
        if status:
            group_change_status(self.current_login_key, status) # 切换小组协作功能的开关
        self.render('group/index.html', group_is_enabled = group_is_enabled(self.current_login_key))
    
