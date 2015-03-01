#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-28 18:07:08
# Filename        : /home/ljd/py/zjypan/admin/settings.py
# Description     : 
from .base import AdminHandler
from public.do import get_settings, save_settings
from lib.wrap import auth_log_save

class AdminSettingsHandler(AdminHandler):
    def get(self, set_obj = None):
        set_obj = set_obj or 'global'
        assert set_obj in ['global', 'file', 'account', 'share'] # account其实是修改用户名密码，里面的数据库会是空的。
        settings = get_settings(set_obj)

        self.render('settings/settings_{set_obj}.html'.format(
            set_obj = set_obj), settings = settings)

    @auth_log_save
    def post(self, set_obj = None):
        """
        输出格式{'mess': 提示信息,'error': 有值表示失败，无值表示成功}
        """
        assert set_obj
        mail_code_verify = get_settings('global').get('verify', True)  # 是否需要 Email验证

        mail_code = self.get_argument('mail_code', '').strip()

        if mail_code_verify and (mail_code != self.session['mail_code'] or mail_code == '' ):
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
        verify = self.get_argument('verify') == 'on'

        assert 60 <= up_time_interval <= 86400 and 1 <= up_num <= 60
        save_settings('global', up_time_interval = up_time_interval,
                up_num = up_num, stop = stop, stop_info = stop_info,
                verify = verify)

        self.write(dict(mess='全局设置已保存～', error=''))
        return '保存全局设置'

    def share_save(self):
        page_limit = int(self.get_argument('page_limit'))
        
        assert 5 <= page_limit <= 50
        save_settings('share', page_limit = page_limit)
        self.write(dict(mess='共享设置已保存', error = ''))
        return '保存共享设置'

    def file_save(self):
        """
        这真是保存文件设置用的。
        """
        expired_day = int(self.get_argument('expired_day', ''))
        add_expired_day = int(self.get_argument('add_expired_day'))

        assert 1 <= expired_day <= 20 and 1 <= add_expired_day <= 10

        save_settings('file', expired_day = expired_day,
                add_expired_day = add_expired_day)

        self.write(dict(mess='文件设置已保存', error=''))
        return '保存文件设置'

    def account_save(self):
        username = self.get_argument('username', '').strip()
        password = self.get_argument('password', '').strip()
        old_password = self.get_argument('old_password', '').strip()

        assert username and password and old_password
        if self.check_user_pass(self.session['username'], old_password) == None:
            self.write(dict(mess='旧密码不匹配，无权修改账号密码', error=1))
            return 

        self.change_user_pass(username, password)
        self.write(dict(mess='用户名密码已更改，请牢记新用户名密码哦～', error=''))
        return '修改账号密码'

