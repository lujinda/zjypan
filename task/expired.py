#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-04-26 15:17:36
# Filename        : task/expired.py
# Description     : 
from .base import TaskHandler
from page.do import FileManager
from time import time

class Expired(TaskHandler):
    def delete(self):
        """
        删除所有已过期的文件
        """
        for file_obj in self.list():
            try:
                file_manager = FileManager(request = self, file_obj = file_obj)
            except FileManager.FileException:
                pass
            else:
                file_manager.expired()

        self.send_result()

    def list(self):
        return self.db.files.find({'expired_time': {'$lt': long(time())}})

