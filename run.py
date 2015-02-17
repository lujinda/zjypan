#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-17 17:20:48
# Filename        : run.py
# Description     : 
from tornado import httpserver, ioloop, web
import logging
from tornado import options
from tornado.options import options, define

from app import PanApplication
import sys
from lib.monitor import MonitorsManager, Monitor

define('port', type=int, default=1234, help='listen port')

if __name__ == "__main__":
    monitors_manager = MonitorsManager()
    sys.stdout = Monitor(monitors_manager, sys.stdout)
    sys.stderr = Monitor(monitors_manager, sys.stderr)
    app = PanApplication(monitors_manager)
    options.parse_command_line()
    http_server = httpserver.HTTPServer(app,
            xheaders=True)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

