# coding: utf-8
# author: LinXin
"""
生成图片的基本设置
"""
from collections import namedtuple
from PIL import Image, ImageFont
from PIL.ImageFont import FreeTypeFont
from typing import Tuple
from os import getcwd


class MyFont:
    """
    实现对字体大小的直接设置
    """
    def __init__(self, path):
        self._path = path
        self._instance = None
        self.size = None

    @property
    def font(self):
        if self._instance is None:
            raise NotImplementedError("必须设置字体大小!")
        return self._instance

    def __setattr__(self, key, value):
        if key == 'size' and value is not None:
            self._instance = ImageFont.truetype(self._path, size=value)
        else:
            super(MyFont, self).__setattr__(key, value)


font = MyFont(r'Sources/UI_Resources/FangZhengYouHei.TTF')
ICON_PATH = r'Sources/Jx3_Datas/skill_icons'

position = namedtuple("position", ['x', 'y'])
size = namedtuple("size", ['width', 'height'])
rgb = namedtuple("rgb", ['r', 'g', 'b'])
rgba = namedtuple("rgba", ['r', 'g', 'b', 'a'])


def get_icon(*, icon_name: str = None, icon_id: int = None, icon_size: Tuple[int, int] = None) -> Image.Image | None:
    """
    根据传入的类型获取对应icon, id会进行网络查询, 名称会进行本地查询\n
    :param icon_size:
    :param icon_name:
    :param icon_id:
    :return img: Image
    """
    icon = None

    # 尝试通过名称获取icon
    if icon_name is not None:
        try:
            icon = Image.open(f"{ICON_PATH}/{icon_name}.png", 'r')
        except FileNotFoundError:
            icon = Image.open(f"{ICON_PATH}/Default.png", 'r')

    # resize
    if icon_size is not None and icon is not None:
        icon = icon.resize(icon_size)

    # icon.show()
    return icon
