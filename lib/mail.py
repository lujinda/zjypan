#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-12 14:34:10
# Filename        : lib/mail.py
# Description     : 

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from os import environ
import smtplib

SMTP_HOST = environ.get('SMTP_HOST', 'smtp.126.com')
SMTP_USER = environ.get('SMTP_USER', 'rupload@126.com')
SMTP_PASS = environ.get('SMTP_PASS', 'zxc123')

class SMTP():
    def __init__(self):
        self._login = False
        self._smtp = smtplib.SMTP()

    def login(self):
        self._smtp.connect(SMTP_HOST)
        self._smtp.ehlo()
        self._smtp.login(SMTP_USER, SMTP_PASS)
        self._login = True

    def send(self, subject, content, mail_addr):
        if isinstance(subject, unicode):
            subject = subject.encode('utf-8')
        if isinstance(subject, unicode): # 不能发送unicode。。
            content = content.encode('utf-8')

        if not self._login:
            self.login()

        msg_root = MIMEMultipart()
        msg_root['Subject'] = subject
        msg_attr = MIMEText(content, _subtype = 'html', _charset = 'utf-8')
        msg_root.attach(msg_attr)
        msg_root['From'] = SMTP_USER
        msg_root['to'] = mail_addr

        self._smtp.sendmail(SMTP_USER, mail_addr.split(';'),
                msg_root.as_string())


def send_mail(subject, content, mail_addr):
    """
    多个email地址间用;分隔
    """
    smtp = SMTP()
    smtp.send(subject, content, mail_addr)

