#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-26 15:03:35
# Filename        : cdn/conf.py
# Description     : 
from ConfigParser import ConfigParser
import os

cfg_path = os.path.join(os.path.dirname(__file__), 'config.cfg')
assert os.path.isfile(cfg_path)

cfg = ConfigParser()
cfg.read(cfg_path)

class CDNConf():
    def __init__(self, section):
        self._section = section
        self.name = section

    def __getattr__(self, option):
        return cfg.get(self._section, option)
def __setattr__(self, option, value):
        """
        不允许修改
        """
        if option not in ('_section', 'name'):
            raise AttributeError
        self.__dict__[option] = value


def get_rand_cdn_conf():
    """
    从配置文件中随机取出一个，随机还没做，至今账号才
    """
    return CDNConf('storage-0')

