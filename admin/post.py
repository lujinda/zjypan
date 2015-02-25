#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-22 21:56:00
# Filename        : admin/post.py
# Description     : 
from .base import AdminHandler
from page.do import write_post, get_post_list, get_post, del_post
from public.do import swith_time
from lib.wrap import auth_log_save

class AdminListPostHandler(AdminHandler):
    def get(self):
        self.render('post/list.html', post_list = get_post_list(), 
                swith_time = swith_time)

    @auth_log_save
    def post(self):
        action = self.get_query_argument('action')
        assert action in ('del', )

        post_uuid_list = self.get_arguments('checked_post')
        assert post_uuid_list

        do_func = getattr(self, 'do_' + action, None)
        self.redirect(self.referer or 'list')
        return do_func(post_uuid_list)

    def do_del(self, post_uuid_list):
        for post_uuid in post_uuid_list:
            del_post(post_uuid)

        return '删除通告'

class AdminWritePostHandler(AdminHandler):
    def get(self):
        post_uuid = self.get_query_argument('post_uuid', '')
        post = get_post(post_uuid)
        self.render('post/write.html', post = post)

    @auth_log_save
    def post(self):
        post_title = self.get_argument('post_title')
        post_content = self.get_argument('post_content')
        post_important = self.get_argument('post_important', None) == 'yes'
        post_uuid =  self.get_argument('post_uuid', None)

        write_post(post_title = post_title, post_content = post_content,
                post_important = post_important, post_uuid = post_uuid)

        self.redirect('list')

        if post_uuid:
            return '编辑通告'
        else:
            return '发布通告'

