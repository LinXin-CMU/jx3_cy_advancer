# coding: utf-8
# author: LinXin
"""
生成配装图
"""
import PIL
from typing import Dict

from CustomClasses.TypeHints import Equip


class EquipPictureCreator:
    """
    生成图片格式复盘的类
    """
    def __init__(self, equip_data: Dict[str, Equip]):
        self._equip_data = equip_data

    def run(self):
        pass