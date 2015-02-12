#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-12 12:09:35
# Filename        : admin/login.py
# Description     : 

from .base import BaseHandler
from code.do import get_code
from lib.wrap import auth_log_save

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html', token = self.token)

    @auth_log_save
    def post(self):
        """
        因为需要记录操作，靠返回值来记录，如果不需要记录，就返回一个空
        """
        token = self.get_argument('token')
        code = self.get_argument('code')
        username = self.get_argument('username')
        password = self.get_argument('password')

        assert token and code and username and password
        if code.lower() != (get_code(token).lower() or '').lower():
            self.write({'error': '验证码不正常，请核对'})
            return 
        
        uid = self.check_user_pass(username, password)

        if uid == None:
            self.write({'error': '用户名与密码不匹配'})
            return '认证失败'


        self.session['uid'] = uid
        self.session['username'] = username
        self.session.save()
        # 为了以后打算，如果要开启账号认证制度，home_page就是用户的主页
        callback_url = self.get_query_argument('callback', self.home_page)
        self.write({'error':'', 'url': callback_url})
        return '登录成功'

