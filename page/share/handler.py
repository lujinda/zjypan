#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-15 20:32:44
# Filename        : page/share/handler.py
# Description     : 

from tornado.web import HTTPError
from public.handler import MyRequestHandler
from page.do import FileManager
from lib.wrap import access_log_save, allow_add_share_num
from lib.oauth import QQLoginOpenApi
from lib import cache
from page.share.do import get_share_file_count, get_share_file, add_share_up_num, add_share_down_num
from page.api.share import ApiShareHandler
from public.do import get_settings
import urllib

class ShareHandler(ApiShareHandler):
    """
    用来处理与单个共享文件有关的东西
    """
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

    def share_download(self):
        share_file = get_share_file(self._share_id)
        if not share_file:
            raise HTTPError(404)
        
        share_url = share_file.get('share_url')
        assert share_url
        self.redirect(share_url)

    @access_log_save
    def post(self, file_key):
        """
        处理添加新共享请求
        """
        share_description = self.get_argument('description')
        share_to_weibo = bool(self.get_argument('share_to_weibo', None))
        self.share_file_key = file_key
        if share_to_weibo and (not self.session.get('openid')):
            self.result_json['error'] = '您还没账号登录，共享到微博失败'
            return

        self.file_manager.share(share_description) # 开始文件共享，会返回share_url
        self.send_result_json()
        if share_to_weibo:
            self.share_to_weibo()

    def share_to_weibo(self):
        openid = self.session.get('openid')
        assert openid

        open_api = QQLoginOpenApi(self.session['access_token'],
                openid)

        file_info = self.file_manager.show_file()
        share_url = "{full_host}/share/download?share_id={share_id}".format(
                full_host = self.full_host(), share_id = file_info.get('share_id'))

        weibo_content = u"我在资源广场分享了: {file_name} {share_url}".format(
            file_name = file_info['file_name'],
            share_url = share_url,
            )
        open_api.send_weibo(weibo_content)

    @access_log_save
    def delete(self, file_key):
        self.share_file_key = file_key
        assert file_key == self.get_argument('file_key') # url中的一定要跟 请求数据中的file_key一致
        self.file_manager.unshare()
        self.write('ok')

    @property
    def file_manager(self):
        share_file_key = self.share_file_key
        share_file_name = self.get_argument('file_name', None)
        file_manager = FileManager(share_file_key, request = self, file_name = share_file_name)
        return file_manager

class ShareSiteHandler(MyRequestHandler):
    def get(self, operation = None):
        condition = ApiShareHandler.get_condition(operation)

        share_file_count = get_share_file_count(condition)
        share_page_limit = self.share_settings.get('page_limit', 16)
        now_page = int(self.get_query_argument('page', 1))

        max_page = share_file_count / share_page_limit + (share_file_count % share_page_limit  and 1 or 0)


        self.render('share/index.html', 
                max_page = max_page, now_page = now_page,
                title = ApiShareHandler._title)
        # self._title 在父类中进行定义


    def post(self, operation = None):
        """
        用于搜索的
        """
        assert operation.startswith('search')
        keyword = self.get_argument('search_keyword').encode('utf-8')

        self.redirect('/share_site/search/' + urllib.quote(keyword))

    @property
    @cache.cache(expired = 7200)
    def share_settings(self):
        return get_settings('share')


class ShareSiteFileHandler(MyRequestHandler):
    def get(self, share_id):
        assert share_id
        
        share_obj = get_share_file(share_id)
        
        self.render('share/file.html', share_obj = share_obj, 
                title = share_obj['file_name'] + u' 详情')

