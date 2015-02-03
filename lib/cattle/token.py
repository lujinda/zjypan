#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-01 14:03:10
# Filename        : cattle/token.py
# Description     : 

from base64 import urlsafe_b64encode
import time
import json
from hashlib import sha1
from base64 import urlsafe_b64encode
import hmac
from urlparse import urlparse

def hmac_sha1_encode(data, secret_key):
    return urlsafe_b64encode(hmac.new(secret_key,
        data, sha1).digest())

class AccessToken():
    def __init__(self, access_key, secret_key, url):
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url

    @property
    def token(self):
        parts = urlparse(self.url)
        token = parts.path
        if parts.query:
            token += ('?' + parts.query)
        token += '\n'
        return ':' .join([self.access_key, 
                hmac_sha1_encode(token, self.secret_key)])

class DownloadToken():
    def __init__(self, access_key, secret_key, url):
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url

    @property
    def token(self):
        checksum = hmac_sha1_encode(self.url, self.secret_key)
        return ':'.join([self.access_key, checksum])



class UploadToken():
    def __init__(self, access_key, secret_key, scope, ttl=3600, fsizeLimt = 0):
        assert ttl > 10
        self.access_key = access_key
        self.secret_key = secret_key
        self.scope = scope
        self.ttl = ttl
        self._token = None
        self._made_token_time = int(time.time())

    @property
    def token(self):
        if self._token == None or int(time.time() - self._made_token_time) < 60:
            self._made_token_time = int(time.time())
            self._token = self._make_token()

        return self._token

    def _make_token(self):
        put_policy = {
                'scope': self.scope, # 如果以<bucket>:<key>指定，表示会被覆盖
                'deadline': self._made_token_time + self.ttl,
                #'fsizeLimit': 0,  # 限制文件上传，这更应该在客户端完成它
                #'detectMime': 0,
                }
        put_policy = json.dumps(put_policy)
        encoded_put_policy = urlsafe_b64encode(put_policy)
        encoded_sign = hmac_sha1_encode(encoded_put_policy, self.secret_key)
        return ':'.join([self.access_key, encoded_sign, encoded_put_policy])

