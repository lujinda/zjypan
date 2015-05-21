#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-04-13 21:18:27
# Filename      : login.py
# Description   : 
from .base import GroupBaseHandler

class GroupLoginHandler(GroupBaseHandler):
    def get(self, message=''):
        self.render('group/login.html', message = message)

    def post(self):
        login_key = self.get_argument('login_key', None)
        if not self.login_key_is_valid(login_key):
            self.get('您的key不是vip，无协作权限')
            return
        
        self.save_login_key(login_key)

        callback = self.get_query_argument('callback', '/group')
        self.redirect(callback) # 如果登录成功后，就重定向到指定的callback上，如果没有就301到协作的首页去

class GroupLogoutHandler(GroupBaseHandler):
    def get(self):
        self.remove_login_key()
        self.redirect('/group/')

