#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-18 13:45:14
# Filename        : run.py
# Description     : 
from tornado import httpserver, ioloop, web
import logging
from tornado import options
from tornado.options import options, define

from app import PanApplication

define('port', type=int, default=1234, help='listen port')

if __name__ == "__main__":
    options.parse_command_line()
    http_server = httpserver.HTTPServer(PanApplication())
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

