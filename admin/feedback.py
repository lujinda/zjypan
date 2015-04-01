#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-06 21:38:20
# Filename        : admin/feedback.py
# Description     : 
from .base import AdminHandler, valid_authenticated
from public.data import db
from public.do import swith_time

def set_feedback_view(feedback):
    uuid = feedback['uuid']

    db.page.feedback.update({'uuid': uuid},
        {'$set': {'view': True}})
    return ''  # 这个函数会在html渲染时执行，不想让它显示什么东西 

def get_feedback_list(condition = {}, skip = 0, limit = 0):
    """
    用来分页地获取feedback_list
    """
    _list = db.page.feedback.find(condition, {'_id': 0}).sort([('time', -1)]).skip(skip).limit(limit)
    return _list

def get_no_views_num():
    return db.page.feedback.find({'view': False}).count()


class AdminFeedbackHandler(AdminHandler):
    @valid_authenticated
    def get(self):
        self.do_list()

    @valid_authenticated
    def post(self):
        action = self.get_query_argument('action')
        func = getattr(self, 'do_' + action)
        func()

    def do_list(self):
        feed_list = get_feedback_list(skip = (self.now_page - 1) * self.page_limit,
                limit = self.page_limit)
        self.render('feedback.html', 
                feedback_list = feed_list, swith_time = swith_time, 
                set_feedback_view = set_feedback_view, 
                now_page = self.now_page, max_page = self.max_page)

    def do_del(self):
        uuid_list = self.get_arguments('uuid')
        for uuid in uuid_list:
            db.page.feedback.remove({'uuid': uuid})

        self.redirect(self.request.path)
        
    @property
    def now_page(self):
        return int(self.get_query_argument('page', 1))

    @property
    def page_limit(self):
        return 20

    @property
    def max_page(self):
        count = get_feedback_list().count()

        return count / self.page_limit + (count % self.page_limit and 1 or 0)


