#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-03 21:19:18
# Filename        : /home/ljd/py/zjypan/admin/settings.py
# Description     : 
from .base import AdminHandler
from public.do import get_settings, save_settings
from public.data import redis_db
from lib.wrap import auth_log_save

class AdminSettingsHandler(AdminHandler):
    def init_data(self):
        self.result_json = {'error': '', 'mess': ''}

    def get(self, set_obj = None):
        set_obj = set_obj or 'global'
        assert set_obj in ['global', 'file', 'account', 'share', 'key'] # account其实是修改用户名密码，里面的数据库会是空的。
        settings = get_settings(set_obj)

        self.render('settings/settings_{set_obj}.html'.format( set_obj = set_obj), settings = settings)

    @auth_log_save
    def post(self, set_obj = None):
        """
        输出格式{'mess': 提示信息,'error': 有值表示失败，无值表示成功}
        """
        assert set_obj
        mail_code_verify = get_settings('global').get('verify', True)  # 是否需要 Email验证

        mail_code = self.get_argument('mail_code', '').strip()

        if mail_code_verify and (mail_code != self.session['mail_code'] or mail_code == '' ):
            self.result_json['mess'] = '保存失败，验证码出错'
            self.result_json['error'] = 1
            self.send_result_json()
            return

        save_func = getattr(self, set_obj + '_save')

        result = save_func()
        self.send_result_json()
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

        self.result_json['mess'] = '全局设置已保存~'
        return '保存全局设置'

    def share_save(self):
        page_limit = int(self.get_argument('page_limit'))
        
        assert 4 <= page_limit <= 40
        save_settings('share', page_limit = page_limit)
        self.result_json['mess'] = '共享设置已保存~'
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

        self.result_json['mess'] = '文件设置已保存~'
        return '保存文件设置'

    def account_save(self):
        username = self.get_argument('username', '').strip()
        password = self.get_argument('password', '').strip()
        old_password = self.get_argument('old_password', '').strip()

        assert username and password and old_password
        if self.check_user_pass(self.session['username'], old_password) == None:
            self.result_json['mess'] = '旧密码不匹配，无权修改'
            self.result_json['error'] = 1
            return 

        self.change_user_pass(username, password)
        self.result_json['mess'] = '用户名密码已更改，请牢记新用户名密码'
        return '修改账号密码'

    def key_save(self):
        """
        维护返回值库
        """
        operation = self.get_argument('operation')
        assert operation in ('add', 'madd', 'del', 'flush')
        key_func= getattr(self, 'key_' + operation)
        return key_func() # 操作返回码的数据库

    def key_flush(self):
        redis_db.delete('key_lib')
        self.result_json['mess'] = '清空Key库成功'
        return '清空Key库'

    def key_add(self):
        key = self.get_argument('key')
        if redis_db.sismember('key_lib', key):
            self.result_json['mess'] = u'%s 已存在' % key
            self.result_json['error'] = 1
            return

        redis_db.sadd('key_lib', key)
        self.result_json['mess'] = u'%s 添加成功' % key
        return u'添加key %s' % key
    
    def key_madd(self):
        key_list = self.get_argument('key_list').split()
        redis_db.sadd('key_lib', *key_list)
        self.result_json['mess'] = u'批量添加成功'
        return u'批量添加key'

    def key_del(self):
        key = self.get_argument('key')
        if redis_db.sismember('key_lib', key):
            redis_db.srem('key_lib', key)
            self.result_json['mess'] = u'%s 删除成功' % key
        else:
            self.result_json['mess'] = u'%s 不存在' % key
            self.result_json['error'] = 1
            return

        return u'删除key %s' % key


