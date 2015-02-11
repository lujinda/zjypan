#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-11 20:51:25
# Filename        : admin/settings.py
# Description     : 
from .base import AdminHandler, valid_authenticated
from public.do import get_settings

class AdminSettingsHandler(AdminHandler):
    @valid_authenticated
    def get(self, set_obj = None):
        set_obj = set_obj or 'global'
        assert set_obj in ['global', 'account']
        settings = get_settings(set_obj)

        self.render('settings/settings_{set_obj}.html'.format(
            set_obj = set_obj), settings = settings)

