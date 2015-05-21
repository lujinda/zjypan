#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-01-06 16:17:42
# Filename        : qr_code.py
# Description     : 

from public.handler import MyRequestHandler
from StringIO import StringIO
from .do import FileManager

def make_qrcode(url):
    import qrcode
    qr = qrcode.QRCode(version=1, border=1)
    qr.add_data(url)
    img = qr.make_image()
    img_fd = StringIO()
    img.save(img_fd)
    img_fd.seek(0)
    return img_fd

class QrcodeHandler(MyRequestHandler):
    def get(self):
        try:
            file_key = self.get_query_argument('file_key')
            file_name = self.get_query_argument('file_name')
            file_manager = FileManager(file_key, self, file_name = file_name)
        except FileManager.FileException as e:
            self.write('key or name error')
            return

        img_fd = make_qrcode(self.made_file_url(file_key, file_name))
        self.add_header('Content-Type','image/png;image/*')
        self.write(img_fd.read())

    def made_file_url(self, file_key, file_name):
        path = '/file.py?file_key=' + file_key + '&file_name=' + file_name
        return u"{protocol}://{host}{path}".format(
                protocol = self.request.protocol, host = self.request.host,
                path = path).encode('utf-8')

