#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-18 21:51:06
# Filename        : app.py
# Description     : 
from tornado.web import Application
from page import FileUpHandler, IndexHandler, FileDownHandler
from module import HeaderModule, FooterModule
from os import path


class PanApplication(Application):
    def __init__(self):
        handlers = [
                (r'/', IndexHandler),
                (r'/up.py', FileUpHandler),
                (r'/down.py', FileDownHandler),
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

