#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-13 02:19:44
# Filename        : page/manage.py
# Description     : 

from .do import FileManager
from public.handler import MyRequestHandler
from lib.wrap import access_log_save

class ManageHandler(MyRequestHandler):
    def init_data(self):
        self.result_json = {'error': '', 'result': []}

    @access_log_save
    def get(self):
        self.render('manage.html')

    @access_log_save
    def post(self):
        try:
            self.file_manager.show()
        except FileManager.FileException, e:
            self.result_json['error'] = e.message
            self.send_result_json()
            return 


    @property
    def file_manager(self):
        file_key = self.get_argument('file_key', '')
        file_name = self.get_argument('file_name', None)
        return FileManager(file_key, self, file_name = file_name)
        
