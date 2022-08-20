from Scripts.ReadData.Equips.equip_type import *
from CustomClasses.TypeHints import Equip

# from typing import Any


class PlayerEquip:
    """
    包含玩家所有装备及装备属性的类
    """

    def __init__(self):
        # self._equip_data: dict = equip
        # 合计属性
        self._attributes = {}
        # 输出属性
        # self.attributes = None
        # 装备属性名序列
        self._equip_name = ["HAT", "JACKET", "BELT", "WRIST", "BOTTOMS", "SHOES", "NECKLACE", "PENDANT", "RING_1",
                            "RING_2", "PRIMARY_WEAPON", "SECONDARY_WEAPON"]


    def __getitem__(self, item) -> Equip | None:
        """
        从PlayerEquip中取出对应位置的方法
        :param item:
        :return:
        """

        if hasattr(self, item):
            return getattr(self, item)
        else:
            return None

    def set_equip(self, origin_equip_info):
        """
        通过lua建立对应装备对象, 并读取装备属性
        :return:
        """
        # print(origin_equip_info[1])
        # 下面开始处理luatable，格式见Documents.JclEquipStructure
        for equip_lua_data in origin_equip_info.values():
            # 对于每一个装备lua
            # 先建立对应装备对象
            try:
                _obj: Equip = position_mapping[equip_lua_data[1]]
                setattr(self, _obj.__name__, _obj(equip_lua_data))
                _equip_obj: Equip = self[_obj.__name__]
                # 针对不同对象设置其基础信息
                _equip_obj.set_info()
            except KeyError as e:
                # 不处理马具飞镖等内容
                print(f"KeyError: {e} at Scripts/ReadData/Equips/equip_reader.py set_equip")
                continue

        # print(*[self[i] for i in self._equip_name])



