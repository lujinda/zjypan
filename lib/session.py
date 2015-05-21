#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-08 20:40:51
# Filename        : lib/session.py
# Description     : 
import uuid
import hmac
import json
import hashlib

class SessionData(dict):
    def __init__(self, session_id, hmac_key):
        self.session_id = session_id
        self.hmac_key = hmac_key

class Session(SessionData):
    def __init__(self, session_manager, request_handler):
        self.session_manager = session_manager
        self.request_handler = request_handler

        try:
            current_session = session_manager.get(request_handler)
        except InvalidSessionException:
            # 如果session有问题，就新建一个session
            current_session = session_manager.get()

        for key, data in current_session.iteritems():
            self[key] = data

        self.session_id = current_session.session_id
        self.hmac_key = current_session.hmac_key

    def save(self):
        self.session_manager.set(self.request_handler, self)

    def logout(self):
        self.session_manager.delete(self.request_handler, self)

class SessionManager(object):
    def __init__(self, session_secret, session_timeout, store_db):
        self.session_secret = session_secret
        self.session_timeout = session_timeout
        self.redis = store_db

    def get(self, request_handler = None):
        session_id = (request_handler and request_handler.get_secure_cookie('session_id')) or self._generate_id()
        hmac_key = (request_handler and request_handler.get_secure_cookie('verification')) or self._generate_hmac(session_id)

        check_hmac = self._generate_hmac(session_id)
        if hmac_key != check_hmac:
            raise InvalidSessionException()

        session = SessionData(session_id, hmac_key)
        session_data = self._fetch(session_id)
        session.update(session_data)
        
        return session

    def _fetch(self, session_id):
        try:
            session_data = raw_data = self.redis.get(session_id)
            if raw_data != None:
                # 用于空闲超时的
                self.redis.setex(session_id, raw_data, self.session_timeout)
                session_data = json.loads(raw_data)

            return isinstance(session_data, dict) and session_data or {}

        except IOError:
            return {}

    def set(self, request_handler, session):
        request_handler.set_secure_cookie('session_id', session.session_id)
        request_handler.set_secure_cookie('verification', session.hmac_key)

        session_data = json.dumps(dict(session.items()))

        self.redis.setex(session.session_id, 
                session_data, self.session_timeout)

    def delete(self, request_handler, session):
        request_handler.clear_cookie('session_id')
        request_handler.clear_cookie('verification')
        self.redis.delete(session.session_id)

    def _generate_id(self):
        new_id = hashlib.sha256(self.session_secret + str(uuid.uuid4()))
        return new_id.hexdigest()

    def _generate_hmac(self, session_id):
        return hmac.new(session_id, self.session_secret, hashlib.sha256).hexdigest()

class InvalidSessionException(Exception):
    pass
        
