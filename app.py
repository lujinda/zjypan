#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-01 21:16:21
# Filename        : app.py
# Description     : 
from tornado.web import Application, StaticFileHandler, RedirectHandler
from code import CodeHandler
from page import FileHandler, IndexHandler, ManageHandler, VerifyHandler, SpeedFileHandler # 用于处理秒传请求
from page.old import OldIndexHandler
from module import HeaderModule, FooterModule, ShareHeaderModule, ShareFooterModule
from os import path
from public.handler import DefaultHandler
from page.api import ApiPostHandler, ApiShareHandler
from page.share import ShareHandler, ShareSiteHandler

from public.data import log_db, db, session_db

class QiniuFileHandler(StaticFileHandler):
    @classmethod
    def make_static_url(cls, settings, path, include_version=True):
        import urlparse
        static_path = settings.get('static_path')
        if not static_path:
            raise Exception
        return urlparse.urljoin(static_path, path)

from admin import LoginHandler, LogoutHandler
from admin import AdminIndexHandler
from module import AdminHeaderModule, AdminFooterModule, AdminLeftModule
from lib.session import SessionManager
from admin.api import ApiOperationHandler, ApiMailCodeHandler, ApiResourcesHandler
from admin.api import ApiCacheHandler
from admin.api import ApiLogHandler
from admin import AdminSettingsHandler
from admin import AdminResourcesHandler
from admin import LogHandler, LogMonitorHandler # 只是用来查看，流量会被打到其他地方
from admin.post import AdminListPostHandler, AdminWritePostHandler

from public.handler import MonitorHandler


class PanApplication(Application):
    def __init__(self, monitors_manager= None):
        handlers = [
                (r'/', IndexHandler),
                (r'/file.py', FileHandler),
                (r'/manage.py', ManageHandler),
                (r'/verify.py', VerifyHandler),
                (r'/code.py', CodeHandler),
                (r'/monitor.py', MonitorHandler),
                (r'/speed_file.py', SpeedFileHandler),
                # 下面uri都不带.py结尾
                (r'/share', ShareHandler), # 只提供对共享文件的操作，如下载，共享，取消共享
                (r'/share_site/?(.*?)', ShareSiteHandler),
                (r'/old/?', OldIndexHandler), # 针对老的浏览器
                (r'/api/post', ApiPostHandler), # 列出特定公告
                (r'/api/share/?(.*?)', ApiShareHandler), # 列出特定共享的文件
                ]

        self.monitors_manager = monitors_manager or []

        settings = {
                'template_path': path.join(path.dirname(__file__), 'template'),
                'static_path': path.join(path.dirname(__file__), 'static'),
               # 'static_path': 'http://7qnb6g.com1.z0.glb.clouddn.com',
               # 'static_handler_class': QiniuFileHandler,
                'ui_modules': {'header': HeaderModule,
                                'footer': FooterModule,
                                'share_header': ShareHeaderModule,
                                'share_footer': ShareFooterModule,
                                },
                'debug': True,
                'gzip': True,
                'cookie_secret': '0a18b23b50ad427d93f7d1d562a446ea',
                'default_handler_class': DefaultHandler,
                }


        self.log_db = log_db
        Application.__init__(self, handlers, **settings)

class PanAdminApplication(Application):
    def __init__(self):
        handlers = [
                (r'/', RedirectHandler, {'url': '/tuxpy'}),
                (r'/code.py', CodeHandler),
                (r'/login.py', LoginHandler),
                (r'/tuxpy/?', AdminIndexHandler),
                (r'/tuxpy/index.py', AdminIndexHandler),
                (r'/tuxpy/logout.py', LogoutHandler),
                (r'/tuxpy/log/(.+?)', LogHandler),
                (r'/tuxpy/settings/(.+)?', AdminSettingsHandler),
                (r'/tuxpy/resources.py', AdminResourcesHandler),
                (r'/tuxpy/monitor.py', LogMonitorHandler),
                (r'/tuxpy/post/list', AdminListPostHandler),
                (r'/tuxpy/post/write', AdminWritePostHandler),
                (r'/api/mailcode', ApiMailCodeHandler),
                (r'/api/operation', ApiOperationHandler),
                (r'/api/resources', ApiResourcesHandler),
                (r'/api/cache', ApiCacheHandler),
                (r'/api/log/(.+?)', ApiLogHandler),
                ]

        settings = {
                'template_path': path.join(path.dirname(__file__), 'template/admin'),
                # 静态文件，像js这些，共享性较大，所以不改
                'static_path': path.join(path.dirname(__file__), 'static'),
                'ui_modules': { 'admin_header': AdminHeaderModule,
                                'admin_footer': AdminFooterModule,
                                'admin_left': AdminLeftModule},
                'debug': True,
                'gzip': True,
                'cookie_secret': '0a18b23b50ad427d93f7d1d562a446ea',
                'login_url': '/login.py',
                }

        session_settings = {
                'session_secret': '0aa48e39-51cf-44c7-b0f2-7b2e1d8277a2',
                'session_timeout': 60 * 500,
                'store_db': session_db,
                }

        self.log_db = log_db
        self.user_db = db
        Application.__init__(self, handlers, **settings)
        self.session_manager = SessionManager(**session_settings)

from task import Expired

class TaskApplication(Application):
    """
    用来跑任务的，比如说文件过期处理和文件与cdn同步等任务。
    """
    def __init__(self):
        handlers = [('/task/expired', Expired),]
        settings = {'debug': True,}

        self.log_db = log_db
        Application.__init__(self, handlers, **settings)

