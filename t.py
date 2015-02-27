#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-26 15:03:39
# Filename        : t.py
# Description     : 

from cdn.conf import get_rand_cdn_conf

c = get_rand_cdn_conf()
print c.sk

