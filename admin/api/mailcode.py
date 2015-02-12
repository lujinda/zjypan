#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-12 14:36:36
# Filename        : admin/api/mailcode.py
# Description     : 
from .base import ApiAdminHandler, api_admin_authenticated
from uuid import uuid4
from lib.mail import send_mail

class ApiMailCodeHandler(ApiAdminHandler):
    """
    发现邮件验证码到作者中去
    """
    @property
    def mail_addr(self): # 用来获取用户的email，目录定是我自己的，为以后开发账号认证机制打算
        return 'q8886888@qq.com'

    @property
    def _rand_code(self):
        """
        生成邮箱验证码
        """
        return uuid4().hex

    def send_mail_code(self):
        self._mail_code = self._rand_code
        send_mail(subject = '您的操作验证码', 
                content = """您的邮箱验证码是<strong>{mail_code}</strong>""".format(mail_code = self._mail_code), mail_addr = self.mail_addr)

    @api_admin_authenticated
    def get(self):
        if self.session.get('mail_code'): # 如果验证码已经发了，就不要去理了
            return
        try:
            self.send_mail_code()
        except:
            # 发送失败再尝试一下
            self.send_mail_code()

        self.session['mail_code'] = self._mail_code
        self.session.save()

