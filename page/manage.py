#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-08 15:32:54
# Filename        : page/manage.py
# Description     : 

from .do import FileManage
from lib.wrap import access_log_save
from public.handler import MyRequestHandler

class ManageHandler(MyRequestHandler):
    result_json = {}

    @access_log_save
    def get(self):
        self.render('manage.html')

    @access_log_save
    def post(self):
        file_key = self.get_argument('file_key', '')
        try:
            file_manage = FileManage(file_key, self)    
        except FileManage.FileException, e:
            self.result_json['error'] = e.message
            self.write_json(self.result_json)
            return 

        file_manage.show()
