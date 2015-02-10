#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-09 13:00:36
# Filename        : public/data.py
# Description     : 

import pymongo
import motor
import redis
import os

motor_client = motor.MotorClient()
mongo_client = pymongo.Connection()
db = mongo_client.zjypan
user_db = db
log_db = motor_client.log

class RedisDb():
    def __init__(self, prefix):
        self._prefix = prefix
        self._db = redis.Redis()
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


redis_db = RedisDb('zjypan_')

def del_local_file(file_path):
    dir_name = os.path.dirname(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        os.removedirs(dir_name)


