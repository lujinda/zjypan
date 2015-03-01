#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-01 22:10:44
# Filename        : page/share/handler.py
# Description     : 

from public.handler import MyRequestHandler
from page.do import FileManager
from lib.wrap import access_log_save
from lib import cache
from page.share.do import get_share_file_count
from page.api.share import ApiShareHandler
from public.do import get_settings

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

    @access_log_save
    def delete(self):
        share_file_key = self.get_argument('file_key')
        file_manager = FileManager(share_file_key, request = self)
        file_manager.unshare()

class ShareSiteHandler(ApiShareHandler):
    def get(self, operation = None):
        condition = self.get_condition(operation)

        share_file_count = get_share_file_count(condition)
        share_page_limit = self.share_settings.get('page_limit', 16)
        now_page = int(self.get_query_argument('page', 1))

        self.render('share/index.html', 
                max_page = (share_file_count / share_page_limit + (share_file_count % share_page_limit  and 1 or 0)), now_page = now_page,
                title = self._title)
        # self._title 在父类中进行定义


    def post(self, operation = None):
        """
        用于搜索的
        """
        assert operation.startswith('search')

        self.redirect('/share_site/search/' + self.get_argument('search_keyword'));

