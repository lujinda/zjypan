#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-15 20:32:44
# Filename        : page/share/handler.py
# Description     : 

from public.handler import MyRequestHandler
from page.do import FileManager
from lib.wrap import access_log_save, allow_add_share_num
from lib import cache
from page.share.do import get_share_file_count, get_share_file, add_share_up_num, add_share_down_num
from page.api.share import ApiShareHandler
from public.do import get_settings
import urllib

class ShareHandler(MyRequestHandler):
    """
    用来处理与单个共享文件有关的东西
    """
    def init_data(self):
        self.result_json = {'error': ''}

    def get(self, operation = None):
        assert operation
        self._share_id = self.get_query_argument('share_id')
        func = getattr(self, 'share_' + operation, None)
        func()
    
    @allow_add_share_num
    def share_up(self):
        """
        为共享文件顶的
        """
        add_share_up_num(self._share_id)
        self.send_result_json()

    @allow_add_share_num
    def share_down(self):
        add_share_down_num(self._share_id)
        self.send_result_json()


    @access_log_save
    def post(self, file_key):
        """
        处理添加新共享请求
        """
        share_description = self.get_argument('description')
        self.share_file_key = file_key

        self.file_manager.share(share_description) # 开始文件共享，并告诉浏览器share_id

    @access_log_save
    def delete(self, file_key):
        self.share_file_key = file_key
        self.file_manager.unshare()

    @property
    def file_manager(self):
        share_file_key = self.share_file_key
        share_file_name = self.get_argument('file_name', None)
        file_manager = FileManager(share_file_key, request = self, file_name = share_file_name)
        return file_manager

class ShareSiteHandler(ApiShareHandler):
    def get(self, operation = None):
        condition = self.get_condition(operation)

        share_file_count = get_share_file_count(condition)
        share_page_limit = self.share_settings.get('page_limit', 16)
        now_page = int(self.get_query_argument('page', 1))

        max_page = share_file_count / share_page_limit + (share_file_count % share_page_limit  and 1 or 0)


        self.render('share/index.html', 
                max_page = max_page, now_page = now_page,
                title = self._title)
        # self._title 在父类中进行定义


    def post(self, operation = None):
        """
        用于搜索的
        """
        assert operation.startswith('search')
        keyword = self.get_argument('search_keyword').encode('utf-8')

        self.redirect('/share_site/search/' + urllib.quote(keyword))

class ShareSiteFileHandler(MyRequestHandler):
    def get(self, share_id):
        assert share_id
        
        share_obj = get_share_file(share_id)
        
        self.render('share/file.html', share_obj = share_obj, 
                title = share_obj['file_name'] + u' 详情')

