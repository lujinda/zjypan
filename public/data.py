#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 21:10:02
# Filename        : public/data.py
# Description     : 

import pymongo
import motor
import redis
import os
from functools import partial

motor_client = motor.MotorClient()
mongo_client = pymongo.Connection()
db = mongo_client.zjypan
db_async = motor_client.zjypan
log_db = motor_client.log
log_db_sync = mongo_client.log

VIP_LIB = 'vip_lib'
KEY_LIB = 'key_lib'

class RedisDb():
    def __init__(self, prefix, db = 0):
        self._prefix = prefix
        self._db = redis.Redis(db = db)
        self.setex = self.set

    def __getattr__(self, func_name):
        if func_name.startswith('__'):
            return getattr(self._db, func_name)
        return partial(self.__prefix_func, func_name)

    def __prefix_func(self, func_name,  name, *args, **kwargs):
        return getattr(self._db, func_name)(self._prefix + name, *args, **kwargs)

    def set(self, name, value, ex = None):
        if ex:
            return self._db.setex(self._prefix + name,
                value, ex)
        else:
            return self._db.set(self._prefix + name, value)
    
    def get(self, name, default = None):
        return self._db.get(self._prefix + name) or default

    def incr(self, name, amount = 1):
        return int(self._db.incr(self._prefix + name,
                amount))


    def keys(self, name='*'):
        return self._db.keys(self._prefix + name)

    def srandmember(self, name, count = 0):
        return self._db.srandmember(self._prefix + name, count)

    def __srand_key(self, name):
        """
        非redis支持，主要用来强化随机，防止有重复的。每次执行后，会移动相应的key到一个备份中，等清空后，就从备份那里把key全复制过来
        """
        set_name = self._prefix + name
        b_set_name = set_name + ':bak'
        pipe = self._db.pipeline()
        pipe.watch(set_name, b_set_name) # 同时监控这两个key，防止数据被中途修改
        _key = pipe.srandmember(set_name)
        pipe.multi()
        if not _key: # 如果_key已经获取不到了，则将b_set_name里面的内容全给set_name, 并删除备份， 并同时再次调用函数本身
            pipe.sunionstore(set_name, b_set_name, set_name)
            pipe.delete(b_set_name)
            pipe.execute()
            return self.__srand_key(name)

        pipe.smove(set_name, b_set_name, _key)
        pipe.execute()

        return _key

    def srand_key(self, name):
        try:
            return self.__srand_key(name)
        except redis.WatchError as e: # 如果是watch错误，就重新调用自己
            return self.srand_key(name)

redis_db = RedisDb('zjypan_')
session_db = redis_db
cache_db = RedisDb('zjypan_cache_')

def del_local_file(file_path):
    dir_name = os.path.dirname(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        try:
            os.removedirs(dir_name)
        except OSError:
            pass
