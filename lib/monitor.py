#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-20 22:25:10
# Filename        : lib/monitor.py
# Description     : 
class Monitor():
    def __init__(self, monitors_manager, std_old):
        self.monitors_manager = monitors_manager
        self.std_old = std_old

    def write(self, buf):
        log = '%s' % buf
        self.std_old.write(log)
        data = {'fileno': self.fileno(),
                'log': log}
        if not self.monitors_manager.empty():
            self.monitors_manager.notify(data)

    def fileno(self):
        return self.std_old.fileno()

class MonitorsManager():
    _callbacks = []
    def register(self, callback):
        self._callbacks.append(callback)

    def unregister(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def notify(self, message):
        for callback in self._callbacks:
            callback(message)

    def empty(self):
        return self._callbacks == []

