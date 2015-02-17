#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-16 20:28:58
# Filename        : public/log.py
# Description     : 

from public.data import log_db_sync
import time

def get_start_stop_time(start, stop=None):
    stop = stop or start
    assert type(start) == type(stop)
    if isinstance(start, time.struct_time):
        return (long(time.mktime(start)), long(time.mktime(stop)) + 86399) # 加上截止那天的日期
    if isinstance(start, (str, unicode)):
        start, stop = map(lambda x:long(time.mktime(time.strptime(x, '%Y-%m-%d'))),
                map(str, [start, stop]))
        stop += 86399
        
        return start, stop
    
    raise

def get_range_log(start = None, stop = None, log_type='file', condition = {}):
    """
    获取指定日期里的日志信息
    """
    if start == None and stop == None:
        return log_db_sync[log_type].find(condition)

    start, stop = get_start_stop_time(start, stop)
    return log_db_sync[log_type].find({'$and': [{'time': {"$gte": start, "$lte": stop}}, 
        condition]})

def operation_log_group(log_type):
    return log_db_sync[log_type].aggregate({'$group': {'_id': "$operation", 
        'count':{'$sum': 1}}}).get('result', [])

def access_log_group():
    return log_db_sync.access.aggregate({"$group": {'_id': '$status_code',
        'count': {'$sum': 1}}}).get('result', [])

