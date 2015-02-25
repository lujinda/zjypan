#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-23 20:19:39
# Filename        : page/manage.py
# Description     : 

from .do import FileManager
from public.handler import MyRequestHandler
from lib.wrap import access_log_save

class ManageHandler(MyRequestHandler):
    result_json = {}

    @access_log_save
    def get(self):
        self.render('manage.html')

    @access_log_save
    def post(self):
        file_key = self.get_argument('file_key', '')
        try:
            file_manage = FileManager(file_key, self)    
        except FileManager.FileException, e:
            self.result_json['error'] = e.message
            self.write_json(self.result_json)
            return 

        file_manage.show()

