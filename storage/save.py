#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-04 19:03:37
# Filename        : storage/save.py
# Description     : 
import os
from public.data import db
from cdn import CDN

def save_to_disk(file_key, file_name, file_body):
    file_path = '/var/tfile/%s/%s' % (file_key, file_name)
    try:
        os.makedirs(os.path.dirname(file_path))
        fd = open(file_path, 'wb')
        fd.write(file_body)
        fd.close()
    except OSError:
        return '目录权限不足', ''

    return '', file_path

def save_to_db(**kwargs):
    """
    作用：一般用于用户文件上传时，把相关信息写到数据库中，待celery将文件上传到云
        必须要保证传入的数据无错
    """
    kwargs['in_cdn'] = kwargs.get('in_cdn') or False
    kwargs['share_id'] = ''

    db.files.insert(kwargs)


# 用于即时同步上传
def save_to_cdn(file_key, file_name, file_path):
    cdn = CDN()
    cdn.put_file(file_key, file_name, file_path)

