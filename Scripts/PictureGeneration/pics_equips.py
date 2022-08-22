# coding: utf-8
# author: LinXin
"""
生成配装图
"""
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Union

from CustomClasses.TypeHints import Equip
from Scripts.PictureGeneration.pics_setting import position, size, rgb


# 位置
EQUIP_ICON_POSITION = position(677, 54)
TALENT_ICON_POSITION = position(103, 472)
ATTRIBUTE_BACKGROUND_POSITION = position(52, 159)
TALENT_BACKGROUND_POSITION = position(52, 435)
EQUIP_BACKGROUND_POSITION = position(651, 30)
# 两个图标之间的间距
EQUIP_ICON_SPACE = 52
TALENT_ICON_VERTICAL_SPACE = 52
TALENT_ICON_HORIZONTAL_SPACE = 160
# 大小
BACKGROUND_SIZE = size(1280, 720)
EQUIP_ICON_SIZE = size(36, 36)
TALENT_ICON_SIZE = size(36, 36)
ATTRIBUTE_BACKGROUND_SIZE = size(545, 245)
TALENT_BACKGROUND_SIZE = size(545, 259)
EQUIP_BACKGROUND_SIZE = size(575, 664)
# 颜色
BACKGROUND_COLOR = rgb(155, 152, 172)
ATTRIBUTE_BACKGROUND_COLOR = rgb(235, 171, 124)
TALENT_BACKGROUND_COLOR = rgb(235, 171, 124)
EQUIP_BACKGROUND_COLOR = rgb(235, 171, 124)


class EquipPictureCreator:
    """
    生成图片格式复盘的类
    """

    def __init__(self, equip_data: Dict[str, Equip]):
        # 装备数据
        self._equip_data = equip_data
        # 背景图
        self.background: Union[Image.Image, None] = None

    def run(self):
        self.background = Image.new('RGB', BACKGROUND_SIZE, BACKGROUND_COLOR)
        self._add_equip_icon([Image.new('RGB', EQUIP_ICON_SIZE, 'white') for _ in range(12)])
        self._add_talent_icon([Image.new('RGB', TALENT_ICON_SIZE, 'white') for _ in range(12)])

    @staticmethod
    def _add_pics(instance):
        """
        确保背景图不为None
        :return:
        """
        _instance = instance
        def wrapper(func):
            def inner(*args, **kwargs):
                ret = None
                if _instance.background is not None:
                    ret = func(*args, **kwargs)
                return ret
            return inner
        return wrapper

    @_add_pics
    def _add_backgrounds(self):
        """
        向背景图添加各部分背景图\n
        :return:
        """


    def _add_equip_icon(self, icons):
        """
        向背景图添加装备图标的方法\n
        :param icons:
        :return:
        """
        pos_y = EQUIP_ICON_POSITION.y
        for index_y in range(12):
            self.background.paste(icons[index_y], (EQUIP_ICON_POSITION.x, pos_y))
            pos_y += EQUIP_ICON_SPACE

    def _add_talent_icon(self, icons):
        """
        向背景图添加奇穴图标的方法\n
        :param icons:
        :return:
        """
        pos_x = TALENT_ICON_POSITION.x
        pos_y = TALENT_ICON_POSITION.y
        for index_x in range(3):
            for index_y in range(4):
                self.background.paste(icons[index_y], (pos_x, pos_y))
                pos_y += TALENT_ICON_VERTICAL_SPACE
            pos_x += TALENT_ICON_HORIZONTAL_SPACE
            pos_y = TALENT_ICON_POSITION.y






if __name__ == '__main__':
    pc = EquipPictureCreator(equip_data=dict())
    pc.run()
    pc.background.show()
