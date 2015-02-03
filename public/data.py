#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-03 17:30:57
# Filename        : public/data.py
# Description     : 

import pymongo
import redis
import os

db = pymongo.Connection().zjypan

class RedisDb():
    def __init__(self, prefix):
        self._prefix = prefix
        self._db = redis.Redis()

    def set(self, name, value, *args, **kwargs):
        return self._db.set(self._prefix + name,
                value, *args, **kwargs)
    
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


