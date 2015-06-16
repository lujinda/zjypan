#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-25 21:34:13
# Filename        : page/do.py
# Description     : 
import time
import string
import random
import os
from public.data import db, del_local_file, redis_db, KEY_LIB, VIP_LIB
from public.do import get_settings, made_uuid
from storage.save import save_to_cdn
from cdn import CDN
import functools
from lib.wrap import file_log_save
from lib.mime import get_file_type
from lib.mail import send_mail
from lib.session import Session
from uuid import uuid4
from tornado.web import HTTPError
from public.handler import MyRequestHandler
from page.group.base import group_is_enabled, item_email_is_exist
from functools import wraps

def valid_login_email_authenticated(func):
    """用来验证已开启小组功能的是否有登录邮箱,应用于FileSessionHandler类"""
    @wraps(func)
    def wrap(self, *args, **kwargs):
        file_key = self.get_file_key()
        if is_vip(file_key) and group_is_enabled(file_key): 
            if not item_email_is_exist(self.current_login_email, file_key):
                raise HTTPError(403)
                return
        return func(self, *args, **kwargs)

    return wrap

class FileSessionHandler(MyRequestHandler):
    """文件类和管理类共有的方法和属性"""
    def init_data(self):
        self.session = Session(self.application.session_manager, self)
        self.result_json = {'error': '', 'result': [], 'error_code': 0}

    @property
    def current_login_email(self):
        return self.session.get(u'{file_key}_login_email'.format(
            file_key = self.get_file_key().decode('utf-8')), u'').lower()

    def get_file_key(self):
        return self.get_argument('file_key', '').encode('utf-8')

    def notify_group_item(self, event_type, file_manage):
        assert event_type in ('download', 'upload', 'delete')
        if not group_is_enabled(self.get_file_key()): # 如果没有开启小组功能的话，就不要通知了
            return
        assert self.current_login_email # 通知必须要有登录的邮箱

        file_info = file_manage.get_file_info() # 获取文件的属性
        file_info['file_url'] = u'%s%s' % (self.full_host(), file_info['file_url'])

        items = list(db.groups.find({'$and': [{'item_email': {'$ne': self.current_login_email}}, 
            {'follow_events': event_type}]}, {'_id': 0})) # 根据不同的事件来选出有监听的成员

        if not items: # 如果没有符合条件的话，就直接返回
            return

        current_item = db.groups.find_one({'file_key': self.get_file_key(), 
            'item_email': self.current_login_email}, {'_id': 0})

        notify_template = 'group/{event}_event_template.html'.format( 
                event = event_type) # 根据不同的事件类型，来指定不同的模块

        notify_content = self.render_string(notify_template,
                current_item = current_item, file_info = file_info)
        mail_addr = map(lambda item: item['item_email'], items)

        send_mail('%s 小组协作有更新了' % (self.get_file_key()),
                notify_content, mail_addr)


class FException(Exception):
    pass

class FileManager():
    """
        这是文件管理器
    """
    FileException = FException
    def __init__(self, file_key = None, request = '', file_name = None, file_obj = None):
        assert file_key or file_obj # 两者必要有一
        self._file_key = file_key or file_obj['file_key']
        self._file_name = file_name  # 供get_file方法使用，如果给定了file_name则会获取具体的文件信息，如果没给定，默认获取第一个
        self.__file = file_obj or self.get_file() # 如果未指定file_name,则获取的是文件中的第一个，指定了就是指定那个
        self.__file_list = file_name == None and self.get_file_list() or [self.__file] # 如果具体指定了某一个文件，则不获取列表了
        self._request = request
        self._cdn = CDN()

        self.is_vip = is_vip(self._file_key)

        if self.is_vip:
            return

        while self.__file and self.__file['expired_time'] < long(time.time()) and self.is_vip == False:
            self.expired()
            self.__file = file_obj  or self.get_file()

        if (not self.__file):
            self.raise_error('文件已不存在')
            return

        # 如果这个文件是存在的话，每一次对它的访问，都会增加日期
        self._add_expired_time()

        self._file_name = self._file_name or self.__file['file_name'] # 如果没有设定file_name的话就根据获取的__file来获取名字，此时__fille已有设定

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
        返回一个与当前file_key和当前file_name匹配的document
        """
        return get_file(file_key = self._file_key, file_name = self._file_name)

    def get_file_list(self):
        return get_file_list(file_key = self._file_key)

    def __delete(self):
        """
        过期删除和主动删除都调用它
        """
        del_local_file(self.__file['file_path'])
        if self.__file['in_cdn']:
            self._cdn.del_file(self._file_key, self._file_name)

        if self.__file['share_id']:
            self.unshare()

        db.files.remove({'file_key':self._file_key, 'file_name': self.__file['file_name']})
     
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
        if self.is_vip:
            return

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
        self.__file['is_vip'] = self.is_vip
        return self.__file

    @file_log_save
    def show(self):
        for __file in self.__file_list:
            self.__file = __file
            file_info = self.show_file()
            if file_info:
                self._request.result_json['result'].append(file_info)
        self._request.send_result_json()

    def show_file(self):
        """
        返回单个文件的信息
        """
        if self.__file['expired_time'] < long(time.time()):
            self.expired()
            return

        file_info = self.get_file_info()

        # 有一些参数不允许被用户看到，就删除
        file_info['can_share'] = file_info['in_cdn']
        for key in ['file_path', 'in_cdn', 'upload_ip']:
            file_info.pop(key, None)

        return file_info


    @file_log_save
    def upload(self):
        save_to_cdn(self._file_key, self._file_name, self.__file['file_path'])
        add_up_total_num()

    @file_log_save
    def speed_upload(self, s_file_key, s_file_name):
        self._cdn.cp(s_file_key, s_file_name, self._file_key, self._file_name)

    @file_log_save
    def share(self, share_decription):
        assert (not self.__file.get('share_id')) and (self.__file['in_cdn'])# 保证还未被共享，并在cdn上

        share_id = uuid4().hex
        share_time = get_now_time()
        share_url = self._cdn.share(self._file_key, self._file_name, share_id)

        # 以下是数据库操作
        db.files.update({'file_key': self._file_key, 'file_name': self._file_name},
                {"$set": {'share_id': share_id}})

        db.share.insert({'share_id': share_id, 'file_name': self._file_name, 
            'share_decription': share_decription,
            'share_time': share_time, 'share_url': share_url, 
            'up_num': 0, 'down_num': 0,
            'file_type': get_file_type(self.__file['content_type'])})
        
        self._request.result_json['share_id'] = share_id
            
    @file_log_save
    def unshare(self):
        """
        成功删除也不返回东西
        """
        share_id = self.__file['share_id']
        share_file_obj = db.share.find_and_modify({'share_id': share_id}, remove = True) # 返回共享信息时，同时删除
        if not share_file_obj: # 如果没有获取到对象的话，表示可能数据库已经被删除了
            return 
        self._file_name = share_file_obj['file_name'] or self.__file['file_name']
        self._cdn.unshare(share_file_obj['share_id'], self._file_name)
        db.files.update({'file_key': self._file_key, 'file_name': self._file_name}, 
                {"$set": {'share_id': ''}})

    def raise_error(self, err_mess):
        raise self.FileException(err_mess)

def get_file(file_key = None, file_md5 = None, file_name = None):
    assert file_key or file_md5
    condition  = {}
    if file_key:
        condition.update({'file_key': file_key})
    if file_name:
        condition.update({'file_name': file_name})

    if file_md5:
        condition.update({'file_md5': file_md5})

    file_obj = db.files.find_one(condition, {'_id': 0})

    return file_obj

def get_file_list(file_key = None):
    return db.files.find({'file_key': file_key}, {'_id': 0}) or []

def get_now_time():
    return long(time.time())

def get_expired_time(new_create = True): # 如果是vip的话，则返回一个夸张的日期
    file_settings = get_settings('file')
    days = new_create and file_settings.get('expired_day', 7) or file_settings.get('add_expired_day', 3)

    return long(time.time() + 24 * 60 * 60 * days)


def made_file_key():
    localtime = time.localtime()
    while True:
        file_key = "%02d%s"%(localtime.tm_mday , 
                redis_db.srand_key('key_lib'))
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


def is_vip(key):
    return bool(redis_db.sismember(VIP_LIB, key))

