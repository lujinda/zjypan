#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-03 15:22:52
# Filename        : page/files.py
# Description     : 
from tornado.web import RequestHandler, asynchronous, HTTPError
from public import error
from .do import made_file_key, get_expired_time, get_upload_time, FileManage, verify_code
from storage.save import save_to_disk, save_to_db

from json_handler import JsonRequestHandler


class FileHandler(JsonRequestHandler):

    """下载的相关代码"""
    def get(self):
        file_key = self.get_argument('file_key', '')
        try:
            file_manage = FileManage(file_key, request = self)
        except FileManage.FileException:
            raise HTTPError(404)

        file_manage.download()
        
    ######################

    """上传的相关代码"""
    @verify_code
    def post(self):
        self.return_json = {'error': ''}
        # 返回的结果都会在这存放
        self.acl.add_visits()

        files = self.request.files['file']
        for f in files:
            self.save_file(f)

        self.write_json(self.return_json)

    def write_error(self, status_code, **kwargs):
        try:
            exc_info = kwargs['exc_info']
            err_message = exc_info[1].log_message
        except:
            err_message = '上传失败'

        self.set_status(status_code)
        self.write({
            'error':err_message,
            })

    """
        作用：对用户上传的文件做出判断，并将相关信息保存到数据库中
        传入: f，格式{'filname':x, 'body':x}
    """
    def save_file(self, f):
        file_size = len(f['body'])
        # 服务器也对文件大小做出判断
        if file_size > 5243380 or file_size == 0:
            self.return_json['error'] = error.FILE_VOLUME_ERROR
            return

        file_key = made_file_key()
        error, file_path = save_to_disk(file_key, f['filename'], f['body'])
        if error:
            self.return_json['error'] = error
            return 

        self.return_json['file_key'] = file_key

        # 当文件都没问题后，就需要把文件信息记录到数据库里了，然后交给celery去上传到云上
        save_to_db(file_key = file_key, file_name = f['filename'], file_path = file_path,
                content_type = f['content_type'],
                upload_ip = self.request.remote_ip, upload_time = get_upload_time(), 
                expired_time = get_expired_time(), file_size = file_size, file_url = '/file.py?file_key=' + file_key)


    ######################
    # 下面是删除文件相关的
    def delete(self):
        file_key = self.get_argument('file_key')
        try:
            file_manage = FileManage(file_key)
            file_manage.delete()
        except FileManage.FileException, e:
            self.write({'error': e.message})

