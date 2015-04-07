#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-04 18:44:53
# Filename        : admin/settings.py
# Description     : 
from .base import AdminHandler
from public.do import get_settings, save_settings
from public.data import redis_db, KEY_LIB, VIP_LIB
from lib.wrap import auth_log_save
import time


class AdminSettingsHandler(AdminHandler):
    def init_data(self):
        self.result_json = {'error': '', 'mess': ''}

    def get(self, set_obj = None):
        set_obj = set_obj or 'global'
        assert set_obj in ['global', 'file', 'account', 'share', 'key', 'vip'] 
        render_func_map = {
                'global'    :   self.render_settings,
                'file'      :   self.render_settings,
                'share'     :   self.render_settings,
                'vip'       :   self.render_vip,
                }
        render_func = render_func_map.get(set_obj, self.render_base)
        render_func(set_obj)

    def render_base(self, set_obj, **kwargs):
        """最普通的页面"""
        self.render('settings/settings_{set_obj}.html'.format(set_obj = set_obj),
                **kwargs)

    def render_settings(self, set_obj):
        """
        需要从数据为中获取设置参数的页面
        """
        settings = get_settings(set_obj)
        self.render_base(set_obj, settings = settings)

    def render_vip(self, set_obj):
        """渲染vip的页面"""
        vip_counts = redis_db.scard(VIP_LIB)
        vip_list = redis_db.smembers(VIP_LIB)

        self.render_base(set_obj, vip_counts = vip_counts, 
                vip_list = vip_list)

    @auth_log_save
    def post(self, set_obj = None):
        """
        输出格式{'mess': 提示信息,'error': 有值表示失败，无值表示成功}
        """
        assert set_obj
        self.result_json['set_obj'] = set_obj
        mail_code_verify = get_settings('global').get('verify', True)  # 是否需要 Email验证

        mail_code = self.get_argument('mail_code', '').strip()

        if mail_code_verify and (mail_code != self.session['mail_code'] or mail_code == '' ):
            self.__send_error('保存失败，验证码出错')
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

        self.__send_success('全局设置已保存~')
        return '保存全局设置'

    def share_save(self):
        page_limit = int(self.get_argument('page_limit'))
        
        assert 4 <= page_limit <= 40
        save_settings('share', page_limit = page_limit)
        self.__send_success('共享设置已保存~')
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

        self.__send_success('文件设置已保存~')
        return '保存文件设置'

    def account_save(self):
        username = self.get_argument('username', '').strip()
        password = self.get_argument('password', '').strip()
        old_password = self.get_argument('old_password', '').strip()

        assert username and password and old_password
        if self.check_user_pass(self.session['username'], old_password) == None:
            self.__send_error('旧密码不匹配，无权修改')
            return 

        self.change_user_pass(username, password)
        self.__send_success('用户名密码已更改，请牢记新用户名密码')
        return '修改账号密码'

    def vip_save(self):
        """
        维护vip账号
        """
        operation = self.get_argument('operation')
        assert operation in ('add', 'del')
        vip = self.get_argument('vip')
        vip_func = getattr(self, 'vip_' + operation)
        self.result_json['operation'] = operation
        self.result_json['vip'] = vip
        return vip_func(vip)

    def vip_add(self, vip):
        if redis_db.sismember(VIP_LIB, vip):
            self.__send_error(u'vip: %s 已存在' % vip)
            return

        if vip[0].encode('utf-8').isdigit():
            self.__send_error(u'vip账号不能以数字开头') # 为了防止与普通的key冲突
            return

        redis_db.sadd(VIP_LIB, vip)

        self.__send_success(u'%s 已成为vip~' % vip)
        return u'添加vip: %s' % vip

    def vip_del(self, vip):
        if not redis_db.sismember(VIP_LIB, vip):
            self.__send_error(u'%s 不是vip' % vip)
            return
        redis_db.srem(VIP_LIB, vip)
        self.__send_success(u'%s 已不是vip' % vip)
        return u'删除vip: %s' % vip

    def key_save(self):
        """
        维护返回值库
        """
        operation = self.get_argument('operation')
        assert operation in ('add', 'madd', 'del', 'flush', 'down')
        key_func= getattr(self, 'key_' + operation)
        return key_func() # 操作返回码的数据库


    def key_down(self):
        key_list = redis_db.smembers(KEY_LIB)

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename="%s_%s"' %
                (time.strftime('%Y-%m-%dT%H:%M:%S'), len(key_list)))
        for key in key_list:
            self.write(key + '\n')

        self.finish()

        return '下载key库'

    def key_flush(self):
        redis_db.delete(KEY_LIB)
        self.__send_success('清空Key库成功')
        return '清空Key库'

    def key_add(self):
        key = self.get_argument('key')
        if redis_db.sismember(KEY_LIB, key):
            self.__send_error(u'%s 已存在' % key)
            return

        redis_db.sadd(KEY_LIB, key)
        self.__send_success(u'%s 添加成功' % key)
        return u'添加key %s' % key
    
    def key_madd(self):
        key_list = self.get_argument('key_list').split()
        redis_db.sadd(KEY_LIB, *key_list)
        self.__send_success( u'批量添加成功')
        return u'批量添加key'

    def key_del(self):
        key = self.get_argument('key')
        if redis_db.sismember(KEY_LIB, key):
            redis_db.srem(KEY_LIB, key)
            self.__send_success( u'%s 删除成功' % key)
        else:
            self.__send_error(u'%s 不存在' % key)
            return

        return u'删除key %s' % key

    def __send_error(self, error):
        self.__send_success(error)
        self.result_json['error'] = 1

    def __send_success(self, error):
        self.result_json['mess'] = error


