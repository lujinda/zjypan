#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-06 19:44:53
# Filename        : page/api/feedback.py
# Description     : 
from public.handler import ApiHandler
from page.do import get_now_time
from lib import cache 
from lib.wrap import allow_feedback
from public.data import db
from public.do import made_uuid

class ApiFeedbackHandler(ApiHandler):
    @allow_feedback
    def post(self):
        content = self.get_argument('content')
        contact = self.get_argument('contact')

        self.write_feedback(content, contact)

        self.result_json['result'] = '谢谢您的反馈'
        self.send_result_json()

    def write_feedback(self, content, contact):
        assert content and contact
        db.page.feedback.insert({'uuid': made_uuid(),'time': get_now_time(),
            'ip': self.client_ip, 'content': content,
            'contact': contact, 'view': False})

