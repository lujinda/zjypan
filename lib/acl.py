#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-06 13:04:50
# Filename        : lib/acl.py
# Description     : 
from public.data import redis_db
from public.do import get_settings
from lib import cache

class ACL():
    def __init__(self, client_ip):
        self._db  = redis_db
        self._client_ip = client_ip
        self.settings_global = get_settings('global')
        self.UP_TIME_INTERVAL = self.settings_global.get('up_time_interval', 5 * 60) # 时间间隔
        self.UP_NUM = self.settings_global.get('up_num', 5) # 记数器限制


    @cache.cache(key = 'need_top')
    def need_stop(self):
        """
        返回(状态，信息)
        """
        return (self.settings_global.get('stop', False),
                self.settings_global.get('stop_info', '系统维护中'))
            

    def need_code(self):
        """
        针对客户端的ip地址来判断是否需要输入验证码，
        需要就返回True
        """
        num = int(redis_db.get(self._client_ip, 0))
        return num >= self.UP_NUM

    def ip_allow(self, allow_ip = '127.0.0.1'):
        return self._client_ip == allow_ip

    def allow_add_share_num(self, share_id):
        """
        返回状态，是否允许评论
        """
        return (not redis_db.get('%s_share_num_%s' % (self._client_ip,
            share_id), None))

    def add_share_num_register(self, share_id):
        redis_db.set("%s_share_num_%s" %(self._client_ip,
            share_id), 1, ex = 86400)

    def allow_feedback(self):
        return not redis_db.get('%s_feedback' % self._client_ip)

    def add_feedback_register(self):
        redis_db.set('%s_feedback' % self._client_ip, 1, ex = 300) # 五分钟内只允许反馈一次


    def add_up_register(self):
        """
        用来记录用户的访问频率的，把当前用户的ip作为记数器
        设置redis中的value，如果已经存在了，就自增加1
        """
        if not redis_db.exists(self._client_ip):
            redis_db.set(self._client_ip, 1, ex = self.UP_TIME_INTERVAL)
        else:
            redis_db.incr(self._client_ip, 1)

    def del_up_register(self): 
        """
        删除用户访问计数器，一般用于验证成功之后
        """
        redis_db.delete(self._client_ip)

