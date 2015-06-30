#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-04-14 21:42:22
# Filename      : manager.py
# Description   : 
from .base import GroupBaseHandler, group_enabled_authenticated, valid_key_authenticated, group_is_enabled, item_email_is_exist
from  public.data import redis_db
from lib.mail import send_mail
import json
import uuid

def write_item_verify_data(item_data):
    """把成员验证信息写入到redis中, 并会添加一个token, 用来审核身份用，token会返回到调用处，通过邮箱发送"""
    token = uuid.uuid4().hex
    item_data['token'] = token
    key = 'group_' + item_data['item_email']
    assert not redis_db.exists(key) # 必须还未存在的
    redis_db.set(key, json.dumps(item_data), 10 * 60)

    return token

def read_item_verify_data(item_email):
    key = 'group_' + item_email
    item_data_json = redis_db.get(key) or '{}'

    return json.loads(item_data_json)

class GroupManagerHandler(GroupBaseHandler):
    """小组协作管理处理类"""
    def __get_opera_func(self):
        opera = self.get_query_argument('opera', None)
        assert opera
        opera_func = getattr(self, opera + '_item', None)
        assert opera_func

        return opera_func

    def get(self):
        """用来处理用户验证, 和用户注销邮箱登录"""
        opera = self.get_query_argument('opera', None)
        assert opera in ['verify', 'leave'] # 只允许激活成员
        opera_func = self.__get_opera_func()
        opera_func()

    def leave_item(self):
        file_key = self.get_query_argument('file_key')
        self.remove_login_email(file_key)
        self.redirect('/manage.py')

    def verify_item(self):
        item_email = self.get_current_item_email()
        token = self.get_query_argument('token', '')

        item_data = read_item_verify_data(item_email)
        verify_token = item_data.pop('token', '')

        if (not self.item_email_is_not_verify(item_email) or (verify_token != token)): # 如果不在未激活列表，可能是过期了, 并且不匹配也是错的
            self.render('group/verify_template.html', mess = 'token有错或已过期')
            return

        redis_db.delete('group_' + item_email)
        self.db.groups.insert(item_data)
        self.render('group/verify_template.html',
                    mess = u'已成功激活，您已是 %s 小组的一员了' % item_data['file_key']) # 激活成功，显示信息

    @valid_key_authenticated
    def post(self):
        opera_func = self.__get_opera_func()
        opera_func()

    def list_item(self):
        items_list = self.get_all_items()
        self.send_result_list(items_list)

    def get_all_items(self):
        return list(self.db.groups.find({'file_key': self.current_login_key}, {'_id': 0}))

    @group_enabled_authenticated
    def add_item(self):
        """添加小组成员, 需要等用户激活后，才能正确加入小组"""
        item_name = self.get_current_item_name()
        item_email = self.get_current_item_email()

        assert item_name and item_email

        if self.item_email_is_not_verify(item_email):
            self.send_result_error('该成员还未邮件激活，请先激活')
            return

        if self.item_email_is_exist(item_email):
            self.send_result_error('该成员email已存在，请重新输入')
            return

        follow_events = self.get_arguments('follow_events', [])

        item_data = {'file_key': self.current_login_key,
            'item_name': item_name, 'item_email': item_email, 
            'follow_events': follow_events} 

        token = write_item_verify_data(item_data)
        mail_content = self.render_string('group/mail_template.html', 
                verify_url = "%s/group/manager?opera=verify&token=%s&item_email=%s" %(
                    self.full_host(), token, item_email), 
                item_data = item_data)
        send_mail("欢迎您使用协同工作", mail_content, item_email)

        self.send_result_success(u"{item_name} {item_email} 添加成功, 请让该用户去邮箱中激活(10分钟内有效)".format(
            item_name = item_name, item_email = item_email))

    @group_enabled_authenticated
    def edit_item(self):
        item_email = self.get_current_item_email()
        if not self.item_email_is_exist(item_email):
            self.send_result_error('该成员不存在，无法编辑')
            return

        item_name = self.get_current_item_name()
        follow_events = self.get_arguments('follow_events', [])

        self.db.groups.update({'file_key': self.current_login_key, 'item_email': item_email},
                {"$set": {'item_email': item_email, 'item_name': item_name, 'follow_events': follow_events}})

        self.send_result_success('成员信息已更新')
    def join_item(self):
        file_key = self.get_argument('file_key', None)
        assert file_key
        item_email = self.get_current_item_email()
        if not group_is_enabled(file_key):
            self.send_result_error('该key未开启小组协作模式')

        if not self.item_email_is_exist(item_email, file_key):
            self.send_result_error('您还未属于该小组，请联系小组负责人')
            return

        if self.item_email_is_not_verify(item_email):
            self.send_result_error('请先激活您的邮箱')
            return

        self.session[u'{file_key}_login_email'.format(
            file_key = file_key)] = item_email  # 以文件file作为session key的前缀以登录登录不同file_key
        self.session.save()

        self.send_result_success('ok')

    @group_enabled_authenticated
    def del_item(self):
        item_email = self.get_current_item_email()
        assert item_email
        if not self.item_email_is_exist(item_email):
            self.send_result_error('该成员已不存在')
            return


        self.db.groups.remove({'file_key': self.current_login_key,
            'item_email': item_email})
        self.send_result_success('删除成功')

    def item_email_is_exist(self, item_email, file_key = None):
        _file_key = file_key or self.current_login_key # 如果是用户加入小组，不会有current_login_key，需要手工传入file_key
        return item_email_is_exist(item_email, _file_key)

    def item_email_is_not_verify(self, item_email):
        return bool(redis_db.get('group_' + item_email))

    def send_result_error(self, error_mess):
        self.__send_result(error_mess, mess_type = 'error')

    def send_result_success(self, success_mess):
        self.__send_result(success_mess, mess_type = 'message')

    def send_result_list(self, result_list):
        self.__send_result(result_list, mess_type = 'result')

    def __send_result(self, message, mess_type):
        """根据类型不同，不发送result"""
        if 'result_json' not in self.__dict__: # 如果还没被定义的话，我先定义一下
            self.result_json = {'error': '', 'message': '', 'result': []}

        self.result_json[mess_type] = message
        self.send_result_json()

    def get_current_item_email(self):
        item_email = self.get_argument('item_email', None)
        assert item_email
        return item_email.lower()

    def get_current_item_name(self):
        item_name = self.get_argument('item_name', None)
        assert item_name
        return item_name

