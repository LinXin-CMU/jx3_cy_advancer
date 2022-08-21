# coding: utf-8
# author: LinXin
"""
生成配装图
"""
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Union
from collections import namedtuple

from CustomClasses.TypeHints import Equip

position = namedtuple("position", ['x', 'y'])

# 装备图标最上方的左上角坐标
EQUIP_ICON_TOP = position(725, 54)
# 奇穴图标坐标
TALENT_ICON_TOP = position(103, 368)
# 两个图标之间的间距
EQUIP_ICON_SPACE = 52
TALENT_ICON_VERTICAL_SPACE = 52
TALENT_ICON_HORIZONTAL_SPACE = 231
# 图标边长
EQUIP_ICON_WIDTH = 36
TALENT_ICON_WIDTH = 36


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
        self.background = Image.new('RGB', (1280, 720), (155, 152, 172))
        self._add_equip_icon([Image.new('RGB', (36, 36), 'white') for _ in range(12)])
        self._add_talent_icon([Image.new('RGB', (36, 36), 'white') for _ in range(12)])

    def _add_equip_icon(self, icons):
        """
        向背景图添加装备图标的方法\n
        :param icons:
        :return:
        """
        if self.background is not None:
            pos_y = EQUIP_ICON_TOP.y
            for index_y in range(12):
                self.background.paste(icons[index_y], (EQUIP_ICON_TOP.x, pos_y))
                pos_y += EQUIP_ICON_SPACE

    def _add_talent_icon(self, icons):
        """
        向背景图添加奇穴图标的方法\n
        :param icons:
        :return:
        """
        if self.background is not None:
            pos_x = TALENT_ICON_TOP.x
            pos_y = TALENT_ICON_TOP.y
            for index_x in range(2):
                for index_y in range(6):
                    self.background.paste(icons[index_y], (pos_x, pos_y))
                    pos_y += TALENT_ICON_VERTICAL_SPACE
                pos_x += TALENT_ICON_HORIZONTAL_SPACE
                pos_y = TALENT_ICON_TOP.y



if __name__ == '__main__':
    pc = EquipPictureCreator(equip_data=dict())
    pc.run()
    pc.background.show()
