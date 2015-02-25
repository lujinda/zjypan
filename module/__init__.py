#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-24 13:03:30
# Filename        : module/__init__.py
# Description     : 
from tornado.web import UIModule

class HeaderModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file)

class FooterModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file)

class AdminHeaderModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file)

class AdminFooterModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file)

class AdminLeftModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file)

