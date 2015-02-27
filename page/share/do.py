#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-27 19:57:39
# Filename        : page/share/do.py
# Description     : 

from public.data import db
from lib.mime import get_file_type

def share_file_type_group():
    """
    返回每种文件的共享数量，并以数量排序返回一个[(x, y), ]列表
    """
    _list = db.share.aggregate({'$group': {'_id':'$content_type',
        'count': {'$sum':1}}}).get('result', [])

    return sorted([(get_file_type(x['_id']), x['count']) for x in _list], 
            key = lambda x:x[1], reverse = True)

