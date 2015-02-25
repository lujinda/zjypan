#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-24 13:25:33
# Filename        : public/data.py
# Description     : 

import pymongo
import motor
import redis
import os

motor_client = motor.MotorClient()
mongo_client = pymongo.Connection()
db = mongo_client.zjypan
db_async = motor_client.zjypan
log_db = motor_client.log
log_db_sync = mongo_client.log

class RedisDb():
    def __init__(self, prefix, db = 0):
        self._prefix = prefix
        self._db = redis.Redis(db = db)
        self.setex = self.set

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


    def exists(self, name):
        return self._db.exists(self._prefix + name)

    def delete(self, name):
        return self._db.delete(self._prefix + name)

    def hset(self, name, key, value):
        return self._db.hset(self._prefix + name, key, value)

    def hgetall(self, name):
        return self._db.hgetall(self._prefix + name)

    def keys(self, name='*'):
        return self._db.keys(self._prefix + name)

    def expire(self, name, expire):
        return self._db.expire(self._prefix + name, expire)


redis_db = RedisDb('zjypan_')
session_db = redis_db
cache_db = RedisDb('zjypan_cache_')

def del_local_file(file_path):
    dir_name = os.path.dirname(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        os.removedirs(dir_name)


