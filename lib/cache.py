#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-15 22:00:51
# Filename        : lib/cache.py
# Description     : 
from public.caches import Page, Cache
from decorator import decorator
from tornado.escape import utf8
from hashlib import md5
try:
    import cPickle as pickle
except ImportError:
    import pickle

def cache(expired = 7200, key = None):
    def wrap(func, self, *args, **kwargs):
        _key = key or (func.__name__ +  self.__class__.__name__ + self.__module__ ) # 定义cache的key，尽可能要做到唯一哦
        _key = key_gen(_key, args, kwargs)
        cache = Cache()
        value = cache.find_cache(_key)
        if value and (value['value']):
            return pickle.loads(value['value'])
        else:
            result = func(self, *args, **kwargs)
            cache.expired = expired
            cache.key = _key
            cache.value = pickle.dumps(result)
            cache.save()
            return result

    return decorator(wrap)

def page(expired = 7200):
    def wrap(method, self, *args, **kwargs):
        key = self.request.uri
        cache = Page()
        value = cache.find_cache(key)

        if value and (value['status'] in (200, 304)) and value['chunk']:
            self.set_status(value['status'])
            self._headers['Content-Type'] = value['headers']['Content-Type']
            self._headers['Set-Cookie'] = value['headers'].get('Set-Cookie', '')
            self.write(utf8(''.join(value['chunk'])))

        else:
            method(self, *args, **kwargs)
            cache.key = key
            cache.status = self._status_code
            cache.headers = self._headers
            cache.chunk = self._buffer
            cache.expired = expired
            cache.save()

    return decorator(wrap)
        

def key_gen(key, args, kwargs):
    """
    生成唯一key，通过md5加密各个参数
    """
    code = md5()
    code. update(str(key))

    c = map(str, args)
    code.update(''.join(c))

    c = ['%s=%s' % (k, v) for k, v in kwargs]
    c.sort()
    code.update(''.join(c))

    return code.hexdigest()

