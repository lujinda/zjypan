#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-03 17:45:06
# Filename        : acl/acl.py
# Description     : 
from public.data import redis_db

class ACL():
    TIME_INTERVAL = 5 * 60 # 时间间隔
    VISITS = 2
    def __init__(self, client_ip):
        self._db  = redis_db
        self._client_ip = client_ip

    # 如果需要验证码的话，会返回True
    def need_code(self):
        visits = int(redis_db.get(self._client_ip, 0))
        return visits >= self.VISITS

    def add_visits(self):
        if not redis_db.exists(self._client_ip):
            redis_db.set(self._client_ip, 1, ex = self.TIME_INTERVAL)
        else:
            redis_db.incr(self._client_ip, 1)

    def del_visits(self):
        redis_db.delete(self._client_ip)

