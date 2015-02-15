#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-15 18:18:48
# Filename        : public/caches.py
# Description     : 
from public.model import RedisModel

class Cache(RedisModel):
    def find_cache(self, key):
        return self.db.hgetall(key)

    def attributes(self):
        return ['key', 'expired', 'value'] 

class Page(Cache):
    def attributes(self):
        return ['key', 'status', 'headers', 'chunk', 'expired']

    def find_cache(self, key):
        _value = {}
        for key, value in self.db.hgetall(key).items():
            if key in ('headers', 'status', 'chunk'):
                _value[key] = eval(value, {})
            else:
                _value[key] = value

        return _value


