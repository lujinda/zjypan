#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-04-13 19:11:08
# Filename      : base.py
# Description   : 
from public.handler import MyRequestHandler
from public.data import redis_db, VIP_LIB, GROUP_LIB, db
from functools import wraps
from lib.session import Session
from tornado.web import HTTPError
from urllib import urlencode

def item_email_is_exist(item_email, file_key):
    return bool(db.groups.find_one({'file_key': file_key,
            'item_email': item_email}))

def group_is_enabled(file_key):
    if not file_key:
        return False
    return bool(redis_db.sismember(GROUP_LIB, file_key))

def group_change_status(file_key, status):
    if status not in ('enable', 'disable'):
        return 
    if status == 'enable':
        redis_db.sadd(GROUP_LIB, file_key)
    else:
        redis_db.srem(GROUP_LIB, file_key)

def group_enabled_authenticated(method):
    @wraps(method)
    def wrap(self, *args, **kwargs):
        if not group_is_enabled(self.current_login_key):
            raise HTTPError(403)
            return
        else:
            return method(self, *args, **kwargs)

    return wrap

def valid_key_authenticated(method):
    @wraps(method)
    def wrap(self, *args, **kwargs):
        if (not self.valid_key()) and (not self.request.path.endswith('login.py')): # 如果不是一个有效的key的话，就会执行重向定到登录key界面
            if self.request.method not in ('GET', 'HEAD'):
                raise HTTPError(403)
                return
            callback_url = self.get_key_login_url() + '?' + urlencode({'callback':
                self.request.uri}) # 如果是GET , HEAD方式来访问的话，如果没有登录成功的话，就会把界面重定向到get_key_login_url的返回值上，并添加参数callback=当前地址
            self.redirect(callback_url)
        else: # 如果登录验证是成功的话，就执行方法
            return method(self, *args, **kwargs)

    return wrap


class GroupBaseHandler(MyRequestHandler):
    def init_data(self):
        self.session = Session(self.application.session_manager, self)

    def login_key_is_valid(self, login_key):
        return bool(redis_db.sismember(VIP_LIB, login_key))

    @property
    def current_login_key(self):
        return self.session.get('login_key', None)

    def remove_login_key(self):
        self.session.pop('login_key', None)
        self.session.save()

    def remove_login_email(self, file_key):
        print(self.session)
        self.session.pop(u'{file_key}_login_email'.format(
            file_key = file_key), None)
        self.session.save()

    def valid_key(self):
        """验证当前key是否具有创建小组的权限"""
        login_key = self.current_login_key
        login_key_by_url = self.get_argument('file_key', None)
        if (not login_key) and (not login_key_by_url):
            return False

        if login_key_by_url:
            login_key = login_key_by_url
            self.save_login_key(login_key)

        return self.login_key_is_valid(login_key) # 判断该key是不是在vip的集合中

    def save_login_key(self, login_key):
        """记住login_key在session中"""
        self.session['login_key'] = login_key
        self.session.save()


    def get_key_login_url(self):
        return '/group/login.py'

    def prepare(self):
        MyRequestHandler.prepare(self)

    @property
    def db(self):
        return db

    def get_template_namespace(self):
        """重写父类的，添加login_key方法"""
        namespace = super(GroupBaseHandler, self).get_template_namespace()
        namespace.update({'current_login_key': self.current_login_key or '未登录'})
        return namespace

