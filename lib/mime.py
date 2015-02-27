#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-02-27 19:43:23
# Filename        : lib/mime.py
# Description     : 

def get_file_type(mime_type):
    """
    根据mime_type返回文件的类型，以中文的方式
    """
    mime_map = {
            'image': '图片',
            'audio': '声音',
            'video': '视频',
            'text': '文本',
            }
    master_type, sub_type = (mime_type.split('/', 1) + [''])[:2]
    file_type = mime_map.get(master_type, None) # 先根据文件大类来确定
    if file_type:
        return file_type
    # 如果不 是这一类的话，一般都是application类的了，这时候就根据小类来确定
    filter_map = {
            'Word文档': ('word', 'works'),
            '电子表格': ('excel',),
            'PPT文档': ('powerpoint', ),
            '压缩包': ('zip', 'tar', 'rar'),
            '种子': ('bittorrent', ),
            '动画': ('flash', ),
            }

    for file_type in filter_map:
        if filter(lambda x : x in sub_type, filter_map[file_type]):
            return file_type

    return '其他'

