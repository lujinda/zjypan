#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-15 20:00:04
# Filename        : page/files.py
# Description     : 
from tornado.web import HTTPError
from .do import made_file_key, get_expired_time, get_now_time, FileManager, get_file # 通过file_key或md5都可以获得文件
from lib.wrap import verify_code
from storage.save import save_to_disk, save_to_db

from public.handler import MyRequestHandler 
from lib.wrap import access_log_save
import urllib

class BaseFileHandler(MyRequestHandler):
    def get_file_key(self):
        return self.get_argument('file_key', '').encode('utf-8')

    def get_file_name(self):
        return self.get_argument('file_name', '').encode('utf-8')

    def rename(self, file_name):
        if not get_file(file_name = file_name, file_key = self.file_key): # 如果文件名和key还未在，就直接返回
            return file_name
        else:
            return self.__rename(file_name)

    def __rename(self, file_name, No = 1):
        """
        用来对文件做自动重名命，防止上传相同的文件
        """
        while True:
            if '.' not in file_name:
                _name = "{file_name}({No})".format(
                        file_name = file_name, No = No)
            else:
                _parts = file_name.split('.')
                _name = "{file_name}({No}).{suffix}".format(
                        file_name = '.'.join(_parts[:-1]), 
                        No = No, suffix = _parts[-1])

            if not get_file(file_name = _name, file_key = self.file_key):
                return _name
            else:
                return self.__rename(file_name, No + 1)

class FileHandler(BaseFileHandler):
    """下载的相关代码"""
    @access_log_save
    def get(self):
        try:
            self.file_manager.download()
        except FileManager.FileException, e:
            print e
            raise HTTPError(404, log_message = e.message)


    ######################

    """上传的相关代码"""
    @access_log_save
    @verify_code
    def post(self):
        self.return_json = {'error': ''} # 返回的结果都会在这存放
        self.acl.add_up_register()

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

    def save_file(self, f):
        """
        作用：对用户上传的文件做出判断，并将相关信息保存到数据库中
        传入: f，格式{'filname':x, 'body':x}
        """
        file_size = len(f['body'])
        # 服务器也对文件大小做出判断
        if file_size > 5243380 or file_size == 0:
            self.return_json['error'] = '文件容量异常'
            return

        file_key = self.get_file_key() or made_file_key() # 如果上传中带有file_key，则表示是新加的
        self.file_key = file_key
        file_name = self.rename(f['filename'].encode('utf-8'))
        error, file_path = save_to_disk(file_key, file_name, f['body'])
        if error:
            self.return_json['error'] = error
            return 

        self.return_json['file_key'] = file_key
        self.return_json['file_name'] = file_name


        # 当文件都没问题后，就需要把文件信息记录到数据库里了，然后交给celery去上传到云上, 计算文件 md5值交给celery去完成
        save_to_db(file_key = file_key, file_name = file_name, file_path = file_path,
                content_type = f['content_type'],
                upload_ip = self.request.remote_ip, upload_time = get_now_time(),
                expired_time = get_expired_time(), file_size = file_size, 
                file_url = '/file.py?file_key=' + file_key + '&file_name=' + file_name)
        self.set_cookie('last_upload', urllib.quote(self.return_json['file_key']))
        file_manager = FileManager(file_key, request = self, file_name = file_name)
        file_manager.upload()


    ######################
    # 下面是删除文件相关的
    @access_log_save
    def delete(self):
        try:
            self.file_manager.delete()
        except FileManager.FileException, e:
            self.write({'error': e.message})

    @property
    def file_manager(self):
        file_manager = FileManager(self.get_file_key(), self, file_name = self.get_file_name())
        return file_manager

class SpeedFileHandler(BaseFileHandler):
    """
    采用md5进行校验
    """
    @verify_code
    def post(self):
        file_md5 = self.get_argument('md5', None)
        exists_file_obj = get_file(file_md5 = file_md5) # 查看是否已存在
        if (not exists_file_obj) or (not exists_file_obj['in_cdn']):
            raise HTTPError(404) # 如果没在cdn上，则发出404错误，让用户把文件上传过来

        file_key = self.get_file_key() or made_file_key() # 如果上传中带有file_key，则表示是新加的
        self.file_key = file_key
        file_name = self.rename(self.get_file_name())

        save_to_db(in_cdn = True, file_key = file_key, file_name = file_name, file_path = '',
                content_type = exists_file_obj['content_type'],
                upload_ip = self.request.remote_ip, upload_time = get_now_time(), file_md5 = file_md5, 
                expired_time = get_expired_time(), file_size = exists_file_obj['file_size'], 
                file_url = '/file.py?file_key=' + file_key + '&file_name=' + file_name)

        file_manage = FileManager(file_key, self, file_name = file_name)
        file_manage.speed_upload(exists_file_obj['file_key'], exists_file_obj['file_name']) # 极速上传，其实就是从已有的进行复制 

        self.acl.add_up_register()

        self.set_cookie('last_upload', urllib.quote(file_key))
        self.write({'error': '', 'file_key' : file_key, 
            'file_name': file_name})

