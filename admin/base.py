#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-11 13:06:34
# Filename        : admin/base.py
# Description     : 

from public.handler import MyRequestHandler
from lib.session import Session
from lib.enc_password import enc_password

class BaseHandler(MyRequestHandler):
    def initialize(self):
        self.session = Session(self.application.session_manager, self)

    @property
    def home_page(self):
        """
            为以后准备，该属性代表着用户的家目录，有普通用户跟管理员之别
        """
        uid = self.session.get('uid', None)
        if uid == None:
            return self.get_login_url()
        if uid == 0:
            return '/tuxpy'

        raise # 留空

    def check_user_pass(self, username, password):
        user_info = self.application.user_db.users.find_one({'username': username,
            'password': enc_password(password)}) or {}
        return user_info.get('uid', None)

class AdminHandler(BaseHandler):
    def create_default(self):
        self.application.user_db.users.update({}, 
                {"$setOnInsert":{'username': 'tuxpy', 'password': enc_password('tuxpy'), 'uid': 0}}, True)

    def get_current_user(self):
        self.create_default()
        return self.session.get('uid') == 0
