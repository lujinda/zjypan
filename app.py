#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-10 20:39:41
# Filename        : app.py
# Description     : 
from tornado.web import Application, StaticFileHandler
from code import CodeHandler
from page import FileHandler, IndexHandler, ManageHandler, VerifyHandler
from module import HeaderModule, FooterModule, AdminHeaderModule, AdminFooterModule, AdminLeftModule
from admin import LoginHandler, LogoutHandler
from admin import AdminIndexHandler
from os import path
from lib.session import SessionManager

from public.data import log_db, user_db, redis_db

class QiniuFileHandler(StaticFileHandler):
    @classmethod
    def make_static_url(cls, settings, path, include_version=True):
        import urlparse
        static_path = settings.get('static_path')
        if not static_path:
            raise Exception
        return urlparse.urljoin(static_path, path)

class PanApplication(Application):
    def __init__(self):
        handlers = [
                (r'/', IndexHandler),
                (r'/file.py', FileHandler),
                (r'/manage.py', ManageHandler),
                (r'/verify.py', VerifyHandler),
                (r'/code.py', CodeHandler),
                (r'/login.py', LoginHandler),
                (r'/tuxpy/?', AdminIndexHandler),
                (r'/tuxpy/index.py', AdminIndexHandler),
                (r'/tuxpy/logout.py', LogoutHandler),
#                (r'/api/'),
                ]

        settings = {
                'template_path': path.join(path.dirname(__file__), 'template'),
                'static_path': path.join(path.dirname(__file__), 'static'),
               # 'static_path': 'http://7qnb6g.com1.z0.glb.clouddn.com',
               # 'static_handler_class': QiniuFileHandler,
                'ui_modules': {'header': HeaderModule,
                                'footer': FooterModule,
                                'admin_header': AdminHeaderModule,
                                'admin_footer': AdminFooterModule,
                                'admin_left': AdminLeftModule},
                'debug': True,
                'gzip': False,
                'cookie_secret': '0a18b23b50ad427d93f7d1d562a446ea',
                'login_url': '/login.py',
                }

        session_settings = {
                'session_secret': '0aa48e39-51cf-44c7-b0f2-7b2e1d8277a2',
                'session_timeout': 60 * 500,
                'store_db': redis_db,
                }

        self.log_db = log_db
        self.user_db = user_db
        Application.__init__(self, handlers, **settings)
        self.session_manager = SessionManager(**session_settings)

