#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-13 14:35:04
# Filename        : admin/base.py
# Description     : 

from public.handler import MyRequestHandler
from lib.session import Session
from lib.enc_password import enc_password
from urllib import urlencode
from functools import wraps
from tornado.web import HTTPError

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

    def change_user_pass(self, username, password):
        # 会根据session中的id值来确定用户的uid
        uid = self.session.get('uid', None)
        assert uid != None
        self.application.user_db.users.update({'uid': uid}, 
                {'$set': {'username': username,
                    'password': enc_password(password)}})

    def check_user_pass(self, username, password):
        print enc_password(password)
        user_info = self.application.user_db.users.find_one({'username': username,
            'password': enc_password(password)}) or {}
        return user_info.get('uid', None)

    def valid_user(self):
        """
        返回当前用户是否是有效的,如果不是，则表示用户认证出错了
        """
        return self.session.get('username')

    def prepare(self):
        """
        重构它是为了使管理员后台不受“维护”影响
        """
        pass

class AdminHandler(BaseHandler):
    def create_default(self):
        self.application.user_db.users.update({}, 
                {"$setOnInsert":{'username': 'tuxpy', 'password': enc_password('tuxpy'), 'uid': 0}}, True)


    def valid_user(self):
        """
        返回当前用户是否是有效的,如果不是，则表示用户认证出错了，管理员id必须是0
        """
        self.create_default()
        return self.session.get('uid') == 0


def valid_authenticated(method):
    """判断用户是否有效，如果无效则重定向到login_url"""
    @wraps(method)
    def wrap(self, *args, **kwargs):
        if not self.valid_user():
            if self.request.method not in ('GET', 'HEAD'):
                raise HTTPError(403)
                return
            callback_url = self.request.uri
            self.redirect(self.get_login_url() + '?' + urlencode({'callback':
                callback_url}))
        else:
            method(self, *args, **kwargs)

    return wrap

