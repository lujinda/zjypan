# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFont
import random
import math, string 
from os import path
from public.data import redis_db
import sys
    
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
 
class RandomChar():
    """用于随机生成汉字"""
    @staticmethod
    def Unicode():
        val = random.randint(0x4E00, 0x4FA5)
        return unichr(val) 

    @staticmethod
    def Letters():
        return random.choice(string.letters)

    @staticmethod
    def GB2312():
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0, 0xF)
        val = ( head << 8 ) | (body << 4) | tail
        str = "%x" % val
        return str.decode('hex').decode('gb2312') 

class ImageChar():
    def __init__(self, fontColor = (0, 0, 0),
                    size = (100, 40),
                    fontPath = path.join(path.dirname(__file__), 'wqy.ttc'),
                    bgColor = (255, 255, 255),
                    fontSize = 22):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGB', size, bgColor) 
 
    def rotate(self):
        self.image.rotate(random.randint(0, 10), expand=100) 
 
    def drawText(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        draw.text(pos, txt, font=self.font, fill=fill)
        del draw 
 
    def randRGB(self):
        return (random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)) 
 
    def randPoint(self):
        (width, height) = self.size
        return (random.randint(0, width), random.randint(0, height)) 
 
    def randLine(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.line([self.randPoint(), self.randPoint()], self.randRGB())
        del draw 
 
    def randChar(self, num):
        gap = 4
        start = 0
        self.code_value = ''
        for i in range(0, num):
            char = RandomChar().Letters()
            self.code_value += char
            x = start + self.fontSize * i + random.randint(0, gap) + gap * i
            self.drawText((x, random.randint(-5, 5)), char, self.randRGB())
            self.rotate()
        self.randLine(10) 
 
    def save(self, path, format=None):
        self.image.save(path, format = format)


# 同时会把token与验证码结果记录到数据库的对应关系中
def get_image_bin(token):
    s_io = StringIO()
    ic = ImageChar()
    ic.randChar(4)
    ic.save(s_io, format='jpeg')
    s_io.seek(0)
    
    redis_db.set(token, ic.code_value, ex = 60)
    
    return s_io.getvalue()

def get_code(token):
    return redis_db.get(token)

