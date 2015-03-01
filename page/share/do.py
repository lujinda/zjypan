#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-28 18:58:14
# Filename        : page/share/do.py
# Description     : 

from public.data import db

def share_file_type_group():
    """
    返回每种文件的共享数量，并以数量排序返回一个[(x, y), ]列表
    """
    _list = db.share.aggregate({'$group': {'_id':'$file_type',
        'count': {'$sum':1}}}).get('result', [])

    return sorted([(x['_id'], x['count']) for x in _list], 
            key = lambda x:x[1], reverse = True)


