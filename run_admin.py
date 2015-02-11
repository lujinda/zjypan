#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-11 14:04:16
# Filename        : run_admin.py
# Description     : 
from tornado import httpserver, ioloop, web
import logging
from tornado import options
from tornado.options import options, define

from app import PanAdminApplication

define('port', type=int, default=1235, help='listen port')

if __name__ == "__main__":
    options.parse_command_line()
    http_server = httpserver.HTTPServer(PanAdminApplication(),
            xheaders=True)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

