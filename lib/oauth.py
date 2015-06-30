#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-16 15:51:51
# Filename      : oauth.py
# Description   : 
import os
from requests import request
import urllib 
import re
import json
from tornado.web import HTTPError

QQ_APP_ID, QQ_APP_KEY, QQ_REDIRECT_URI = os.environ.get('QQ_APP_ID'), \
        os.environ.get('QQ_APP_KEY'), os.environ.get("QQ_REDIRECT_URI")

assert QQ_APP_ID and QQ_APP_KEY and QQ_REDIRECT_URI


class QQLoginOpenApi(object):
    def __init__(self, access_token, openid, oauth_consumer_key = None):
        self.__public_request_data = {
                'access_token'      :   access_token,
                'openid'            :   openid,
                'oauth_consumer_key':   oauth_consumer_key or QQ_APP_ID,
                'format'            :   'json',
                }

    def send_weibo(self, content):
        url = 'https://graph.qq.com/t/add_t'
        request_data = {
                'content'       :   content,
                }
        self.__api_call(url, request_data, 'POST')

    def __api_call(self, url, data, method = 'GET'):
        data.update(self.__public_request_data)
        r = request(url = url, data = data, method = method, verify = None)

class PublicOAuthLoginServer(object):
    def __init__(self, handler, code):
        self.handler = handler
        self.code = code

    def start_oauth_login(self):
        self.get_access_token()

    def get_access_token(self):
        request_url = self.access_token_url
        request_data = {
                "grant_type"    :   "authorization_code",
                "client_id"     :   self.app_id,
                "client_secret" :   self.app_key,
                "code"          :   self.code,
                "redirect_uri"  :   self.redirect_uri,
                }

        self.handler.async_request(request_url + '?' + urllib.urlencode(request_data), 
                self.token_callback)

    def token_callback(self, response):
        """在获取access_token后，会调它 """
        raise ImportError


    def urldecode(self, param):
        if not param:
            return {}
        arguments = {}
        for _item in param.split('&'):
            if '=' not in _item:
                continue
            _k, _v = _item.split('=', 1)
            arguments[_k] = _v

        return arguments 

class QQOAuthLoginServer(PublicOAuthLoginServer):
    app_id = QQ_APP_ID
    app_key = QQ_APP_KEY
    redirect_uri = QQ_REDIRECT_URI
    access_token_url = "https://graph.qq.com/oauth2.0/token" 

    def token_callback(self, response):
        return self.get_open_id(response)

    def get_open_id(self, response):
        if response.error:
            raise HTTPError(response.code)
        response_data = self.urldecode(response.body)

        access_token = response_data['access_token']
        self.handler.session['access_token'] = access_token
        request_url = "https://graph.qq.com/oauth2.0/me?access_token=" + access_token

        self.handler.async_request(request_url, self.get_user_info)


    def get_user_info(self, response):
        if response.error:
            raise HTTPError(response.code)

        response_data = self.urldecode(response.body)
        self.handler.session['openid'] = response_data['openid']

        request_url = "https://graph.qq.com/user/get_user_info"
        request_data = {
                'access_token'          :       self.handler.session['access_token'],
                'oauth_consumer_key'    :       self.app_id,
                'openid'                :       self.handler.session['openid'],
                'format'                :       'json',
                }

        self.handler.async_request(request_url + '?'+ urllib.urlencode(request_data),
                self.finish_oauth)

    def finish_oauth(self, response):
        if response.error:
            raise HTTPError(response.code)

        response_data = json.loads(response.body)
        self.handler.session['nickname'] = response_data['nickname']
        self.handler.session['figureurl'] = response_data['figureurl']

        self.handler.session.save()
        self.handler.redirect('/')

    def urldecode(self, param):
        if not param:
            return {}
        json_str = (re.findall('.*({.*}).*', param) or [{}])[0]
        if not json_str:
            return super(QQOAuthLoginServer, self).urldecode(param)

        return json.loads(json_str) 
    
oauth_server_map = { 'openapi.qzone.qq.com'  :   QQOAuthLoginServer}

