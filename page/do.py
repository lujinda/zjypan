#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-26 22:03:01
# Filename        : page/do.py
# Description     : 
import time
import string
import random
import os
from public.data import db, del_local_file, redis_db
from public.do import get_settings, made_uuid
from storage.save import save_to_cdn
from cdn import CDN
import functools
from lib.wrap import file_log_save
from uuid import uuid4


class FException(Exception):
    pass

class FileManager():
    """
        这是文件管理器
    """
    FileException = FException
    def __init__(self, file_key = None, request = '', file_obj = None):
        assert file_key or file_obj # 两者必要有一
        self._file_key = file_key or file_obj['file_key']
        self._request = request
        self.__file = file_obj or self.get_file()
        self._cdn = CDN()
        if (not self.__file):
            self.raise_error('文件已不存在')
            return

        if self.__file['expired_time'] < long(time.time()):
            self.expired()
            self.raise_error('文件已过期')
            return

        # 如果这个文件是存在的话，每一次对它的访问，都会增加日期
        self._add_expired_time()

    def _add_expired_time(self):
        """
        每次初始化FileManager时，都会把到期时间加ADD_EXPIRED_DAY天
        """
        old_expired_time = self.__file['expired_time']
        new_expired_time = get_expired_time(False)

        # 如果原先的过期时间比新的过期时间早的话，才更新过期时间，要不然就不更新
        if old_expired_time > new_expired_time:
            return

        self.__file['expired_time'] = new_expired_time
        db.files.update({'file_key':self._file_key}, 
                {"$set": {'expired_time': new_expired_time}})

    def get_file(self):
        """
        返回一个与当前file_key匹配的document
        """
        return get_file(file_key = self._file_key)

    def __delete(self):
        """
        过期删除和主动删除都调用它
        """
        del_local_file(self.__file['file_path'])
        if self.__file['in_cdn']:
            self._cdn.del_file(self.__file['file_key'], self.__file['file_name'])

        db.files.remove({'file_key':self._file_key})
     
    @file_log_save
    def delete(self):
        """
        删除文件document, 本地文件，云上的文件
        """
        self.__delete()

    @file_log_save
    def expired(self):
        """
        过期删除调用，同delete,只是日志记录不同而已
        """
        self.__delete()

    @file_log_save
    def download(self):
        # 如果文件已经在网盘上存在了，就重定向到网盘
        if self.__file['in_cdn']:
            cdn_url = self._cdn.get_cdn_url(self._file_key,
                    self.__file['file_name'])
            self._request.redirect(cdn_url)
            return

        self._request.set_header('Content-Type', 'application/octet-stream')
        self._request.set_header('Content-Disposition', 'attachment; filename="%s"' % 
                self.__file['file_name'])

        try:
            fd = open(self.__file['file_path'], 'rb')
            while True:
                data = fd.read(4096)
                if not data:
                    break
                self._request.write(data)
            fd.close()
        except:
            self._request.set_status(404)
        finally:
            self._request.finish()
        

    def get_file_info(self):
        self.__file['file_size'] = switch_unit(self.__file['file_size'])
        return self.__file

    @file_log_save
    def show(self):
        if self.__file['expired_time'] < long(time.time()):
            self.raise_error('文件已过期')
            return

        file_info = self.get_file_info()

        # 有一些参数不允许被用户看到，就删除
        for key in ['file_path', 'in_cdn', 'upload_ip']:
            del file_info[key]

        self._request.write_json(file_info)


    @file_log_save
    def upload(self):
        save_to_cdn(self.__file['file_key'], self.__file['file_name'], self.__file['file_path'])
        add_up_total_num()

    @file_log_save
    def speed_upload(self, s_file_key, s_file_name):
        self._cdn.cp(s_file_key, s_file_name, self.__file['file_key'], self.__file['file_name'])

    @file_log_save
    def share(self, share_decription):
        assert (not self.__file.get('share_id')) and (self.__file['in_cdn'])# 保证还未被共享，并在cdn上

        share_id = uuid4().hex
        share_time = get_now_time()
        share_url = self._cdn.share(self.__file['file_key'], self.__file['file_name'], share_id)

        # 以下是数据库操作
        db.files.update({'file_key': self._file_key},
                {"$set": {'share_id': share_id}})

        db.share.insert({'share_id': share_id, 'file_name': self.__file['file_name'], 
            'share_decription': share_decription,
            'share_time': share_time, 'share_url': share_url, 
            'content_type': self.__file['content_type']})

        self._request.write({'error': '', 'share_id': share_id}) # 需要修改

    def raise_error(self, err_mess):
        raise self.FileException(err_mess)

def get_file(file_key = None, file_md5 = None):
    assert file_key or file_md5
    if file_key:
        condition = {'file_key': file_key}
    if file_md5:
        condition = {'file_md5': file_md5}

    file_obj = db.files.find_one(condition, {'_id': 0})
    return file_obj

def get_now_time():
    return long(time.time())

def get_expired_time(new_create = True):
    file_settings = get_settings('file')
    days = new_create and file_settings.get('expired_day', 7) or file_settings.get('add_expired_day', 3)

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

def get_save_total_num():
    """
    获取当前有多少文件存在服务器上
    """
    return db.files.count()


def add_up_total_num():
    redis_db.incr('up_total_num', 1)

def get_up_total_num():
    return redis_db.get('up_total_num', 0)
    
def write_post(**kwargs):
    """
    用于更新或写新通知
    """
    post_uuid = kwargs.get('post_uuid')
    if not post_uuid:
        kwargs['post_time'] = long(time.time())
        post_uuid = made_uuid()
        kwargs['post_uuid'] = post_uuid

    db.page.post.update({'post_uuid': post_uuid}, 
            {'$set': kwargs}, True)

def get_post_list(skip = 0, limit = 0):
    return db.page.post.find({}, {'_id': 0, 'post_content': 0}).skip(skip).limit(limit)

def get_post(post_uuid):
    return db.page.post.find_one({'post_uuid': post_uuid}) or {}

def del_post(post_uuid):
    return db.page.post.remove({'post_uuid': post_uuid})

