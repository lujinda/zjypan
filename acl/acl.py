#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-03 18:40:08
# Filename        : acl/acl.py
# Description     : 
from public.data import redis_db

class ACL():
    TIME_INTERVAL = 5 * 60 # 时间间隔
    VISITS = 2 # 记数器限制
    def __init__(self, client_ip):
        self._db  = redis_db
        self._client_ip = client_ip

    def need_code(self):
        """
        针对客户端的ip地址来判断是否需要输入验证码，
        需要就返回True
        """
        visits = int(redis_db.get(self._client_ip, 0))
        return visits >= self.VISITS

    def add_visits(self):
        """
        用来记录用户的访问频率的，把当前用户的ip作为记数器
        设置redis中的value，如果已经存在了，就自增加1
        """
        if not redis_db.exists(self._client_ip):
            redis_db.set(self._client_ip, 1, ex = self.TIME_INTERVAL)
        else:
            redis_db.incr(self._client_ip, 1)

    def del_visits(self):
        """
        删除用户访问计数器，一般用于验证成功之后
        """
        redis_db.delete(self._client_ip)

