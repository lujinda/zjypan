#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-18 11:54:55
# Filename        : run.py
# Description     : 
from tornado import httpserver, ioloop, web
import logging
from tornado import options

from app import PanApplication

if __name__ == "__main__":
    options.parse_command_line()
    http_server = httpserver.HTTPServer(PanApplication())
    http_server.listen(1234)
    ioloop.IOLoop.instance().start()

