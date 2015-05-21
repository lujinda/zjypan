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
from threading import Thread

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
        if not isinstance(mail_addr, (list, tuple)):
            raise TypeError

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
        msg_root['to'] = ';'.join(mail_addr)

        self._smtp.sendmail(SMTP_USER, mail_addr,
                msg_root.as_string())


def send_mail(subject, content, mail_addr):
    """
    多个email地址间用;分隔
    """
    if not isinstance(mail_addr, (tuple, list)): # 如果传入的邮件是不是多个的,不是以列表或元组存在的，则将它传转一下
        mail_addr = mail_addr.split(';')

    smtp = SMTP()
    send_mail_thread = Thread(target = smtp.send, args = (subject, content, mail_addr))
    send_mail_thread.setDaemon(True)
    send_mail_thread.start()

