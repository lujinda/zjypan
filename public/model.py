#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-15 21:04:30
# Filename        : public/model.py
# Description     : 

from public.data import cache_db

class RedisModel(dict):
    def __init__(self):
        self['_record'] = {}
        
    @property
    def db(self):
        return cache_db

    def attributes(self):
        raise NotImplementedError

    def record(self):
        return self['_record']

    def __setattr__(self, key, value):
        assert key in self.attributes()
        self.record()[key] = value

    def __getattr__(self, key):
        assert key in self.attributes()
        return self.record().get(key, None)

    def save(self):
        key = self.record().pop('key')
        expired = self.record().pop('expired', 7200)
        for k, v in self.record().items():
            self.db.hset(key, k, v)

        self.db.expire(key, expired)

    def flush(self):
        map(self.db._db.delete, self.db.keys()) # _db 是没有经过封装的数据库

