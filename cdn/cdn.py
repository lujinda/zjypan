#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-07 12:09:56
# Filename        : cdn/cdn.py
# Description     : 
from celery import Celery
from celery.contrib.methods import task_method
import time
from lib.cattle import Cattle
from public.data import db, del_local_file
from functools import partial
import urllib
import os

BROKER_URL = 'redis://127.0.0.1:6379/15'


celery = Celery('CDN', broker = BROKER_URL)

class CDN():
    def __init__(self):
        self._bucket_name = 'zjypan-0'
        self._domain = '7u2qd9.com1.z0.glb.clouddn.com'
        self._cattle = Cattle('BbDU4MoFrx2YaF6tqBFmnKHFuDlq1EO-mm2ldlBm', 'WWdwgm4oRmOh_L9yKbyWplcUFaIGAZXk8e_UOtDs')

    @celery.task(filter=task_method)
    def sync(self):
        print 'ok'
        print 'end'

    def get_cdn_url(self, file_key, file_name):
        if isinstance(file_name, unicode):
            # 在获取七牛私有下载地址前，要对key做url转义
            file_name = urllib.quote(file_name.encode('utf-8'))
            file_key = file_key.encode('utf-8')

        base_url = 'http://%s/%s' %(self._domain, '%s/%s' % (file_key, file_name))
        private_url = self._cattle.private_url(base_url)
        return private_url

    @celery.task(filter=task_method)
    def put_file(self, file_key, file_name, file_path):
        if isinstance(file_name, unicode):
            file_name = file_name.encode('utf-8')
            file_key = file_key.encode('utf-8')

        ret, error = self._cattle.put_file(self._bucket_name,
                file_path, "%s/%s" % (file_key, file_name),
                mime_type = 'application/octet-stream')
        if error:
            return

        # 上传完后，再判断一下是否在上传的过程中被删除了。
        if not os.path.exists(file_path):
            self.del_file(file_key, file_name)
            return

         #当上传成功后，把信息修改一下
        db.files.update({'file_key': file_key}, {"$set": {'in_cdn': True}})
        
        # 然后把本地文件删除一下
        del_local_file(file_path)       

    @celery.task(filter=task_method)
    def del_file(self, file_key, file_name):
        if isinstance(file_name, unicode):
            file_name = file_name.encode('utf-8')
            file_key = file_key.encode('utf-8')

        ret, error = self._cattle.rm(self._bucket_name,
                '%s/%s' % (file_key, file_name))

