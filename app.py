#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-06 20:21:10
# Filename        : app.py
# Description     : 
from tornado.web import Application, StaticFileHandler
from code import CodeHandler
from page import FileHandler, IndexHandler, ManageHandler, VerifyHandler
from module import HeaderModule, FooterModule
from os import path

from public.data import log_db

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
                ]

        settings = {
                'template_path': path.join(path.dirname(__file__), 'template'),
                'static_path': path.join(path.dirname(__file__), 'static'),
                'ui_modules': {'header': HeaderModule,
                                'footer': FooterModule},
                'debug': True,
                'gzip': True,
                'cookie_secret': '0a18b23b50ad427d93f7d1d562a446ea',
                }

        self.log_db = log_db
        Application.__init__(self, handlers, **settings)


