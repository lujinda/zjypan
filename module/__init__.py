#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-17 17:22:45
# Filename        : module/__init__.py
# Description     : 
from tornado.web import UIModule

class HeaderModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file)

class FooterModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file)

