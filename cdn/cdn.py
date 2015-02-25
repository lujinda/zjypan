#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-25 18:44:03
# Filename        : cdn/cdn.py
# Description     : 
from celery import Celery
from celery.contrib.methods import task_method
import time
from lib.cattle import Cattle
from public.data import db, del_local_file
from functools import partial
from lib.enc import get_file_md5
import urllib
import os

BROKER_URL = 'mongodb://127.0.0.1:27017/celery'


celery = Celery('CDN', broker = BROKER_URL)

def made_cdn_key(file_key, file_name, quote = False):
    """
    生成cdn可以用的key，做一些编码工作什么的
    """
    if isinstance(file_key, unicode):
        file_key = file_key.encode('utf-8')

    if isinstance(file_name, unicode):
        file_name = file_name.encode('utf-8')

    if quote:
        file_name = urllib.quote(file_name)

        
    return '%s/%s' %(file_key, file_name)

class CDN():
    def __init__(self):
        self._bucket_name = 'zjypan-0'
        self._domain = '7u2qd9.com1.z0.glb.clouddn.com'
        self._cattle = Cattle('BbDU4MoFrx2YaF6tqBFmnKHFuDlq1EO-mm2ldlBm', 'WWdwgm4oRmOh_L9yKbyWplcUFaIGAZXk8e_UOtDs')

    @celery.task(filter=task_method)
    def sync(self):
        print 'ok'
        print 'end'

    def cp(self, s_file_key, s_file_name, d_file_key, d_file_name):
        ret, error = self._cattle.cp(self._bucket_name,
                made_cdn_key(s_file_key, s_file_name), made_cdn_key(d_file_key, d_file_name))
        assert not error


    def get_cdn_url(self, file_key, file_name):
        base_url = 'http://%s/%s' %(self._domain, made_cdn_key(file_key, file_name, True))
        private_url = self._cattle.private_url(base_url)
        return private_url

    @celery.task(filter=task_method)
    def __put_file(self, file_key, file_name, file_path):
        ret, error = self._cattle.put_file(self._bucket_name,
                file_path, made_cdn_key(file_key, file_name),
                mime_type = 'application/octet-stream')
        if error:
            return

        file_md5 = get_file_md5(file_path)

        # 上传完后，再判断一下是否在上传的过程中被删除了。
        if (not os.path.exists(file_path)) or (not file_md5):
            self.del_file(file_key, file_name)
            return

         #当上传成功后，把信息修改一下
        db.files.update({'file_key': file_key}, {"$set": {'in_cdn': True, 
            'file_md5': file_md5}})
        
        # 然后把本地文件删除
        del_local_file(file_path)       


    @celery.task(filter=task_method)
    def __del_file(self, file_key, file_name):
        ret, error = self._cattle.rm(self._bucket_name,
                made_cdn_key(file_key, file_name))

    def put_file(self, *args, **kwargs):
        self.__put_file.delay(*args, **kwargs)

    def del_file(self, *args, **kwargs):
        self.__del_file.delay(*args, **kwargs)

