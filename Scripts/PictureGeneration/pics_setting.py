# coding: utf-8
# author: LinXin
"""
生成图片的基本设置
"""
from collections import namedtuple


FONT = r'Sources/UI_Resources/FangZhengYouHei.TTF'

position = namedtuple("position", ['x', 'y'])
size = namedtuple("size", ['width', 'height'])
rgb = namedtuple("rgb", ['r', 'g', 'b'])
rgba = namedtuple("rgba", ['r', 'g', 'b', 'a'])
