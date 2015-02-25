#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-04-26 14:59:30
# Filename        : run_task.py
# Description     : 
from tornado import httpserver, ioloop, options
from app import TaskApplication
from tornado.options import options, define

define('port', type = int, help = "listen in given port", default = 1236)

if __name__ == '__main__':
    options.parse_command_line()
    app = TaskApplication()
    http_server = httpserver.HTTPServer(app, 
            xheaders = True)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

