#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-27 19:53:24
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

from page.share.do import share_file_type_group

class ShareHeaderModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file, 
                share_file_type_list = share_file_type_group())

class ShareFooterModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file)

