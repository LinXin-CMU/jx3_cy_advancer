# coding: utf-8
# author: LinXin
"""
生成配装图
"""
from PIL import Image
from PIL.ImageDraw import ImageDraw
from typing import Dict, List, Union

from CustomClasses.TypeHints import Equip
from Scripts.PictureGeneration.pics_setting import position, size, rgb, get_skill_icon, font, get_equip_icon


# 位置
ATTRIBUTE_BACKGROUND_POSITION = position(52, 159)
TALENT_ICON_POSITION = position(103, 472)
EQUIP_ICON_POSITION = position(677, 54)
TALENT_BACKGROUND_POSITION = position(52, 435)
EQUIP_BACKGROUND_POSITION = position(651, 30)
# 两个图标之间的间距
EQUIP_ICON_SPACE = 52
TALENT_ICON_VERTICAL_SPACE = 52
TALENT_ICON_HORIZONTAL_SPACE = 160
TALENT_ICON_TEXT_HORIZONTAL_SPACE = 20   # 奇穴图标到奇穴文本间距离
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
# 圆角
BACKGROUNDS_RADIUS = 10
# 字号
TALENT_TEXT_SIZE = 25

BACKGROUNDS = (
    (ATTRIBUTE_BACKGROUND_POSITION, ATTRIBUTE_BACKGROUND_SIZE, ATTRIBUTE_BACKGROUND_COLOR),
    (EQUIP_BACKGROUND_POSITION, EQUIP_BACKGROUND_SIZE, EQUIP_BACKGROUND_COLOR),
    (TALENT_BACKGROUND_POSITION, TALENT_BACKGROUND_SIZE, TALENT_BACKGROUND_COLOR)
)


class EquipPictureCreator:
    """
    生成图片格式复盘的类
    """

    def __init__(self):
        # 装备数据
        self._equip_data = None
        # 背景图
        self.background: Union[Image.Image, None] = None
        # 背景图ImageDraw实例化
        self._background: ImageDraw | None = None
        # 实例方法装饰器
        self._decorator()

    def set_equip_data(self, equip_data: Dict[str, Equip]):
        self._equip_data = equip_data

    def run(self, talent: List[str]):
        if self._equip_data is not None:
            self.background = Image.new('RGB', BACKGROUND_SIZE, BACKGROUND_COLOR)
            self._add_backgrounds()
            self._add_equip_icon([Image.new('RGB', EQUIP_ICON_SIZE, 'white') for _ in range(12)])
            self._add_talent_icon(talent)
            self.background.show()


    def _check_background(self, func):
        """
        确保背景图不为None
        :return:
        """
        def inner(*args, **kwargs):
            ret = None
            # print('inside')
            if self.background is not None:
                ret = func(*args, **kwargs)
            return ret
        return inner

    def _decorator(self):
        """
        给实例方法添加实例装饰器\n
        :return:
        """
        self._add_backgrounds = self._check_background(self._add_backgrounds)
        self._add_equip_icon = self._check_background(self._add_equip_icon)
        self._add_talent_icon = self._check_background(self._add_talent_info)


    def _add_backgrounds(self):
        """
        向背景图添加各部分背景图\n
        :return:
        """
        self._background = ImageDraw(self.background)
        for _position, _size, _color in BACKGROUNDS:
            _right_bottom = position(_position.x + _size.width, _position.y + _size.height)
            self._background.rounded_rectangle((_position, _right_bottom), fill=_color, radius=BACKGROUNDS_RADIUS, width=0)

    def _add_equip_icon(self, icons):
        """
        向背景图添加装备图标的方法\n
        :return:
        """
        pos_y = EQUIP_ICON_POSITION.y
        for index_y in range(12):
            self.background.paste(icons[index_y], (EQUIP_ICON_POSITION.x, pos_y))
            pos_y += EQUIP_ICON_SPACE
        get_equip_icon(icon_id=[i.equip_data['_IconID'] for i in self._equip_data.values() if i is not None])


    def _add_talent_info(self, talent_list: List[str]):
        """
        向背景图添加奇穴图标和文本的方法\n
        :param icons:
        :return:
        """
        pos_x = TALENT_ICON_POSITION.x
        pos_y = TALENT_ICON_POSITION.y
        icons = [get_skill_icon(icon_name=i, icon_size=TALENT_ICON_SIZE) for i in talent_list]
        font.size = TALENT_TEXT_SIZE
        for index_x in range(3):
            for index_y in range(4):
                self.background.paste(icons[index_y + index_x*4], (pos_x, pos_y))
                self._background.text((pos_x + TALENT_ICON_SIZE.width + TALENT_ICON_TEXT_HORIZONTAL_SPACE, pos_y+3), talent_list[index_y+index_x*4], font=font.font)
                pos_y += TALENT_ICON_VERTICAL_SPACE
            pos_x += TALENT_ICON_HORIZONTAL_SPACE
            pos_y = TALENT_ICON_POSITION.y





#
# if __name__ == '__main__':
#     pc = EquipPictureCreator(equip_data=dict())
#     pc.run()
#     pc.background.show()
