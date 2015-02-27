#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-27 19:10:41
# Filename        : page/share/handler.py
# Description     : 

from public.handler import MyRequestHandler
from page.do import FileManager
from lib.wrap import access_log_save

class ShareHandler(MyRequestHandler):
    def get(self):
        pass

    @access_log_save
    def post(self):
        """
        处理添加新共享请求
        """
        share_description = self.get_argument('description')
        share_file_key = self.get_argument('file_key')

        file_manager = FileManager(share_file_key, request = self)
        file_manager.share(share_description) # 开始文件共享，并告诉浏览器share_id

class ShareSiteHandler(MyRequestHandler):
    def get(self, operation):
        self.render('share/index.html')

