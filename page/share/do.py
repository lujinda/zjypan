#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-02 19:54:27
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

def get_share_file_count(conditon = {}):
    return db.share.find(conditon).count()

def get_share_file(share_id):
    return db.share.find_one({'share_id': share_id})

def add_share_up_num(share_id):
    db.share.update({'share_id': share_id}, {"$inc": {'up_num': 1} })

def add_share_down_num(share_id):
    db.share.update({'share_id': share_id}, {'$inc': {'down_num': 1}} )

