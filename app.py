#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-25 14:25:00
# Filename        : app.py
# Description     : 
from tornado.web import Application
from page import FileHandler, IndexHandler, ManageHandler
from module import HeaderModule, FooterModule
from os import path

class PanApplication(Application):
    def __init__(self):
        handlers = [
                (r'/', IndexHandler),
                (r'/file.py', FileHandler),
                (r'/manage.py', ManageHandler),
                ]

        settings = {
                'template_path': path.join(path.dirname(__file__), 'template'),
                'static_path': path.join(path.dirname(__file__),
                                    'static'),
                'ui_modules': {'header': HeaderModule,
                                'footer': FooterModule},
                'debug': True,
                }

        Application.__init__(self, handlers, **settings)

