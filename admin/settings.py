#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-12 16:02:21
# Filename        : admin/settings.py
# Description     : 
from .base import AdminHandler, valid_authenticated
from public.do import get_settings, save_settings

class AdminSettingsHandler(AdminHandler):
    @valid_authenticated
    def get(self, set_obj = None):
        set_obj = set_obj or 'global'
        assert set_obj in ['global', 'account']
        settings = get_settings(set_obj)

        self.render('settings/settings_{set_obj}.html'.format(
            set_obj = set_obj), settings = settings)

    @valid_authenticated
    def post(self, set_obj = None):
        """
        返回格式{'mess': 提示信息,'error': 有值表示失败，无值表示成功}
        """
        assert set_obj
        mail_code = self.get_argument('mail_code', '').strip()

        if mail_code != self.session['mail_code'] or mail_code == '':
            self.write(dict(mess='保存失败，验证码出错', error=1))
            return

        save_func = getattr(self, set_obj + '_save')

        result = save_func()
        self.session.pop('mail_code', None) # 如果验证成功的话，就可以把mail_code删掉了
        self.session.save()
        return result

    def global_save(self):
        up_time_interval = int(self.get_argument('up_time_interval'))
        up_num = int(self.get_argument('up_num'))
        stop = self.get_argument('stop') == 'on'
        stop_info = self.get_argument('stop_info', '')

        assert 60 <= up_time_interval <= 86400 and 1 <= up_num <= 60
        save_settings('global', up_time_interval = up_time_interval,
                up_num = up_num, stop = stop, stop_info = stop_info)

        self.write(dict(mess='全局设置已保存～', error=''))
        return '保存全局设置'

