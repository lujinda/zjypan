#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-13 02:19:44
# Filename        : page/manage.py
# Description     : 

from .do import FileManager, FileSessionHandler
from public.handler import MyRequestHandler
from public.data import db
from public.error import NEED_LOGIN_EMAIL
from lib.wrap import access_log_save
from page.group.base import group_is_enabled, item_email_is_exist
from lib.session import Session

class ManageHandler(FileSessionHandler):
    @access_log_save
    def get(self):
        self.render('manage.html')

    @access_log_save
    def post(self):
        if group_is_enabled(self.get_file_key()): # 如果已经启动了小组功能
            if not (self.current_login_email and item_email_is_exist(self.current_login_email, self.get_file_key())):
                self.send_result_error('该key已成功开启小组协作，请先登录您的邮箱', NEED_LOGIN_EMAIL)
                return
            self.result_json['login_email'] = self.current_login_email
        try:
            self.file_manager.show()
        except FileManager.FileException, e:
            self.send_result_error(e.message)
            return 

    @property
    def file_manager(self):
        return FileManager(self.get_file_key(), self, file_name = self.file_name)

    @property
    def file_name(self):
        return self.get_argument('file_name', None)

    def send_result_error(self, error_mess, error_code=0):
        self.result_json['error'] = error_mess
        self.result_json['error_code'] = error_code
        self.send_result_json()

