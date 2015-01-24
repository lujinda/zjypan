#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-24 21:00:50
# Filename        : page/manage.py
# Description     : 

from .do import FileManage
from json_handler import JsonRequestHandler

class ManageHandler(JsonRequestHandler):
    result_json = {}

    def get(self):
        self.render('manage.html')

    def post(self):
        file_key = self.get_argument('file_key', '')

        try:
            file_manage = FileManage(file_key)    
        except FileManage.FileException, e:
            self.result_json['error'] = e.message
            self.write_json(self.result_json)
            return 

        file_manage.get_file_info()

