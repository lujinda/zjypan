#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-24 21:01:14
# Filename        : page/do.py
# Description     : 
import time
import string
import random
from public.data import db


class FileManage():
    FileException = Exception
    def __init__(self, file_key):
        self.__file_key = file_key
        self.__file = self.get_file()
        if not self.__file:
            self.raise_error('文件已不存在')

    def get_file(self):
        return db.files.find_one({'file_key': self.__file_key})

    def get_file_info(self):
        print self.__file

    def raise_error(self, err_mess):
        raise self.FileException(err_mess)


def get_upload_time():
    return long(time.time())

def get_expired_time(days = 3):
    return long(time.time() + 24 * 60 * 60 * 3)



# 返回文件的一些信息，如文件大小，文件类型什么的
def get_file_info(file_key):
    file_obj = get_file(file_key)
    return file_obj

def made_file_key():
    localtime = time.localtime()
    while True:
        file_key = "%2d%s%s%s"%(localtime.tm_mday , localtime.tm_wday + 1 , \
                random.choice(string.ascii_letters) , random.choice(string.ascii_letters))
        if not db.files.find_one({'file_key': file_key}):
            break

    return file_key

