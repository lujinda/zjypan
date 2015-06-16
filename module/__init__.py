#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-06 20:01:05
# Filename        : module/__init__.py
# Description     : 
from tornado.web import UIModule
from admin.feedback import get_no_views_num
from lib.oauth import QQ_APP_ID, QQ_REDIRECT_URI
import os

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
        return self.render_string(render_file, no_views_num = get_no_views_num()) 
from page.share.do import share_file_type_group

class ShareHeaderModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file, 
                share_file_type_list = share_file_type_group())

class ShareFooterModule(UIModule):
    def render(self, render_file):
        return self.render_string(render_file)

class QQLoginModule(UIModule):
    def render(self):
        client_id, redirect_uri = QQ_APP_ID, QQ_REDIRECT_URI
        return self.render_string('qq_login.html', client_id = client_id,
                redirect_uri = redirect_uri,
                state = self.handler.token, scope = "get_user_info,add_t")

