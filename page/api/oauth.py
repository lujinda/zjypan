#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-15 17:56:11
# Filename      : oauth.py
# Description   : 
from public.handler import ApiHandler
from tornado.web import HTTPError
from lib.oauth import oauth_server_map
from urlparse import urlsplit
import os 


class QQOAuthCallbackHandler(ApiHandler):
    def get(self):
        code = self.get_query_argument('code')
        if not code:
            raise HTTPError(403, "Miss code")

        state = self.get_query_argument('state')
        if not state == self.token:
            raise HTTPError(403, "state error")


        openid = self.session.get('openid')
        if not openid:
            self.start_oauth_login(code)
        else:
            self.redirect('/')

    def start_oauth_login(self, code):
        """根据不同的Referer，来判断是哪家服务商并开始oauth登录"""
        referer = self.request.headers.get('Referer')
        if not referer:
            raise HTTPError(403)
        server_host = urlsplit(referer).netloc
        oauth_server = oauth_server_map.get(server_host)
        if not (oauth_server):
            raise HTTPError(403)
        oauth_server = oauth_server(self, code)
        oauth_server.start_oauth_login()

class QQUserInfoHandler(ApiHandler):
    def get(self):
        nickname = self.session.get('nickname')
        figureurl = self.session.get('figureurl')
        if not (nickname and figureurl):
            self.result_json['status_code'] = 404
            self._send_result()
        else:
            self._send_result({
                'nickname'      :       nickname,
                'figureurl'     :       figureurl,
                })
            self._send_result()

    def delete(self):
        for _key in  ['nickname', 'figureurl', 'access_token', 'openid']:
            self.session.pop(_key, None)
        self.session.save()


