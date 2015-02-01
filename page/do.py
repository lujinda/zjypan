#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-01 14:28:09
# Filename        : page/do.py
# Description     : 
import time
import string
import random
import os
from public.data import db, del_local_file
from tornado.web import HTTPError
from cdn import CDN

class FException(Exception):
    pass

class FileManage():
    FileException = FException
    def __init__(self, file_key, request = ''):
        self.__file_key = file_key
        self.__request = request
        self.__file = self.get_file()
        if (not self.__file):
            self.raise_error('文件已不存在')
            return
        # 如果这个文件是存在的话，每一次对它的访问，都会增加日期
        self._add_expired_time()
        self._cdn = CDN()

    def _add_expired_time(self):
        old_expired_time = self.__file['expired_time']
        new_expired_time = get_expired_time(3)

        # 如果原先的过期时间比新的过期时间早的话，才更新过期时间，要不然就不更新
        if old_expired_time > new_expired_time:
            return

        self.__file['expired_time'] = new_expired_time
        db.files.update({'file_key':self.__file_key}, 
                {"$set": {'expired_time': new_expired_time}})

    def get_file(self):
        file_obj = db.files.find_one({'file_key': self.__file_key})
        if file_obj:
            del file_obj['_id']
        return file_obj
     
    def delete(self):
        del_local_file(self.__file['file_path'])
        if self.__file['in_cdn']:
            self._cdn.del_file.delay(self.__file['file_key'], self.__file['file_name'])

        db.files.remove({'file_key':self.__file_key})

    def download(self):
        # 如果文件已经在网盘上存在了，就重定向到网盘
        if self.__file['in_cdn']:
            cdn_url = self._cdn.get_cdn_url(self.__file['file_key'],
                    self.__file['file_name'])
            self.__request.redirect(cdn_url)
            return

        self.__request.set_header('Content-Type', 'application/octet-stream')
        self.__request.set_header('Content-Disposition', 'attachment; filename="%s"' % 
                self.__file['file_name'])

        try:
            fd = open(self.__file['file_path'], 'rb')
            while True:
                data = fd.read(4096)
                if not data:
                    break
                self.__request.write(data)
            fd.close()
        except:
            self.__request.set_status(404)
        finally:
            self.__request.finish()
        

    def get_file_info(self):
        self.__file['file_size'] = switch_unit(self.__file['file_size'])
        return self.__file

    def raise_error(self, err_mess):
        raise self.FileException(err_mess)


def get_upload_time():
    return long(time.time())

def get_expired_time(days = 7):
    return long(time.time() + 24 * 60 * 60 * days)


def made_file_key():
    localtime = time.localtime()
    while True:
        file_key = "%02d%s%s%s"%(localtime.tm_mday , localtime.tm_wday + 1 , \
                random.choice(string.ascii_letters) , random.choice(string.ascii_letters))
        if not db.files.find_one({'file_key': file_key}):
            break

    return file_key

# 转换文件大小单位，方便阅读
def switch_unit(size):
    def b_mode():
        return size

    def k_mode():
        return size / 1000.0
    
    def m_mode():
        return k_mode() /  1000.0

    import math

    unit_list = ['B', 'KB', 'MB']
    unit_func = {'B': b_mode, 'KB': k_mode, 'MB': m_mode}
    unit = unit_list[int(math.log10(size)) /  3]
    return "%.2f%s" % (unit_func[unit](), unit)

