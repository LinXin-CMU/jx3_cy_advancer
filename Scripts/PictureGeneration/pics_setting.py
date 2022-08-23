# coding: utf-8
# author: LinXin
"""
生成图片的基本设置
"""
import os
from collections import namedtuple

import requests
from PIL import Image, ImageFont
from PIL.ImageFont import FreeTypeFont
from typing import Tuple, List
from os import getcwd
from concurrent.futures import ThreadPoolExecutor, as_completed


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


pool = ThreadPoolExecutor(12)
equip_icons = [i.replace('.png', '') for i in os.listdir(r'Sources/Jx3_Datas/equip_icons') if i.endswith('.png')]



def get_equip_icon(*, icon_id: List[int] = None, icon_size: Tuple[int, int] = None) -> List[Image.Image]:
    global pool, equip_icons

    def task(icon_id):
        resp = requests.get(rf'https://icon.jx3box.com/icon/{icon_id}.png', timeout=3)
        if resp.status_code == 200:
            return resp.content, icon_id

    all_tasks = [pool.submit(task, i) for i in icon_id if str(i) not in equip_icons]
    for future in as_completed(all_tasks):
        try:
            _pic, _id = future.result()
            with open(rf'Sources/Jx3_Datas/equip_icons/{_id}.png', 'wb') as f:
                f.write(_pic)
        except TypeError as e:
            print(f"TypeError: {e} at Scripts/PictureGeneration/pics_setting.py get_equip_icon: 图标id不存在或网络异常")
    ret = []
    for _id in icon_id:
        try:
            _icon = Image.open(rf'Sources/Jx3_Datas/equip_icons/{_id}.png', 'r')
        except FileNotFoundError:
            _icon = Image.open(r'Sources/Jx3_Datas/equip_icons/Default.png', 'r')
        if icon_size is not None:
            _icon = _icon.resize(icon_size)
        ret.append(_icon)
    return ret




def get_skill_icon(*, icon_name: str = None, icon_id: int = None, icon_size: Tuple[int, int] = None) -> Image.Image | None:
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
