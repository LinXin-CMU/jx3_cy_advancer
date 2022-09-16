from re import compile

from Sources.Jx3_Datas.Files.jx3_stone import stone
from Sources.Jx3_Datas.Files.jx3_equip import equip
from Sources.Jx3_Datas.Files.jx3_enchant import enchant
from Sources.Jx3_Datas.Files.get_other_data import get_equip_from_jx3box


class _Equip:
    """存放装备信息的基类"""

    def __init__(self, data) -> None:
        self.data = data  # jcl中的data信息串
        self.equip_data: dict | None = None  # equip库中该装备的数据

        self.id = data[3]
        self.strength: int = data[4]  # 精炼
        self.max_strength_level = None  # 最大精炼等级
        self.embedding = None  # 镶嵌
        self.enhance = None  # 小附魔
        self.enhance_name = None
        self.enchant = None  # 大附魔
        self.stone = None  # 五彩石

        # 一切可被jcl读取到的基础属性
        self.attrs = {
            'BaseAttrs': {},
            'MagicAttrs': {},
        }
        # 精炼、镶嵌、大小附魔
        self.changed_attrs = {
            'BaseAttrs': {},
            'MagicAttrs': {},
        }
        self.subtype = None  # 子类型. 即表的名称
        self.name = None
        self.equip_type = None  # 散件/精简/无皇/特效
        self.level = None  # 品级
        self.attr_type = None  # 简要属性，_Attrs

    def set_name(self):
        """
        20220731针对精炼镶嵌页面额外补充
        :return:
        """
        self.name = f"{self.equip_data['Name']}({self.strength})"

    def set_info(self):
        """针对不同装备的特点记录属性"""
        # 源数据信息
        try:
            self.equip_data = equip[self.subtype][self.id]
        except KeyError as e:
            # 未查询到则返回未知装备
            print(f"KeyError: not found id={e} equip at Scripts/ReadData/Equips/equip_type.py set_info")
            self.equip_data = get_equip_from_jx3box(self.subtype, self.id)['Data']
            print(f"get equip data from personal_data: {self.equip_data['Name']}")
        # 查找名称，品级，最大精炼
        if self.equip_data is not None:
            # 20220729装备栏精炼镶嵌不能正常读取
            self.name = f"{self.equip_data['Name']}"
            self.level = self.equip_data["Level"]
            self.max_strength_level = int(self.equip_data['MaxStrengthLevel'])

        # 五彩石
        if self.stone is not None:
            try:
                stone_id = self.data[5][0][2]
            except TypeError:
                print("无五彩石！")
            else:
                try:
                    if not stone_id == 0 and stone_id is not None:
                        try:
                            stone_info = stone[stone_id]
                        except KeyError:
                            stone_info = None
                            stone_name = '五彩石等级过低'
                        else:
                            stone_name = ''
                            stone_lv = None
                            for index, attr_info in enumerate(stone_info):
                                if len(stone_info) == 3:
                                    # 常规五彩石
                                    if index == 0:
                                        if attr_info[4] == '11':
                                            stone_lv = '(肆)'
                                        elif attr_info[4] == '13':
                                            stone_lv = '(伍)'
                                        elif attr_info[4] == '14':
                                            stone_lv = '(陆)'
                                elif len(stone_info) == 2:
                                    # 精简五彩石
                                    if index == 0:
                                        if attr_info[4] == '12':
                                            stone_lv = '(肆)'
                                        elif attr_info[4] == '14':
                                            stone_lv = '(伍)'
                                        elif attr_info[4] == '16':
                                            stone_lv = '(陆)'
                                if len(attr_info[0]) == 5:
                                    stone_name += attr_info[0][3:]
                                elif attr_info[0] == '武器伤害':
                                    stone_name += "武伤"
                                else:
                                    stone_name += attr_info[0]
                                stone_name += '·'
                            stone_name = stone_name[:-1] + stone_lv
                    else:
                        stone_info = None
                        stone_name = '无五彩石'
                    self.stone = {'name': stone_name, 'data': stone_info}
                except KeyError as e:
                    print(f"KeyError: {e} at Scripts/ReadData/Equips/equip_type.py stone")

        # 装备自身属性
        # 基础属性
        for i in range(1, 7):
            # Base{n}Attribute 1-6
            if self.equip_data[f"Base{i}Type"] is not None and not self.equip_data[f"Base{i}Type"] == "atInvalid":
                # 如果该基础属性不为None且不为非法属性
                if self.equip_data[f"Base{i}Type"] not in self.attrs['BaseAttrs']:
                    self.attrs['BaseAttrs'][self.equip_data[f"Base{i}Type"]] = max(int(self.equip_data[f"Base{i}Max"]), int(self.equip_data[f"Base{i}Min"]))
                else:
                    self.attrs['BaseAttrs'][self.equip_data[f"Base{i}Type"]] += max(int(self.equip_data[f"Base{i}Max"]), int(self.equip_data[f"Base{i}Min"]))
                # 在BaseAttrs中添加该属性字段及数值
        # 魔法属性
        for i in range(1, 13):
            # _Magic{n}Type 1-12
            if self.equip_data[f"_Magic{i}Type"] is not None:
                # 如果该魔法属性不为None
                _attr = self.equip_data[f"_Magic{i}Type"]['attr']
                try:
                    if _attr[0] not in self.attrs['MagicAttrs']:
                        self.attrs['MagicAttrs'][_attr[0]] = max(int(_attr[1]), int(_attr[2]))
                    else:
                        self.attrs['MagicAttrs'][_attr[0]] += max(int(_attr[1]), int(_attr[2]))
                except TypeError:
                    if _attr[0] not in self.attrs['MagicAttrs']:
                        self.attrs['MagicAttrs'][_attr[0]] = max(int(_attr[3]), int(_attr[4]))
                    else:
                        self.attrs['MagicAttrs'][_attr[0]] += max(int(_attr[3]), int(_attr[4]))
        # print("")

        # 装备额外属性



    def read_embedding_and_strength(self):
        """
        计算精炼和镶嵌值
        :return:
        """
        # 清空属性
        self.changed_attrs = {
            'BaseAttrs': {},
            'MagicAttrs': {},
        }

        # 精炼
        # 常量表
        refine = [0, 0.005, 0.013, 0.024, 0.038, 0.055, 0.075, 0.098, 0.124]
        # 对于每一个魔法属性
        for attr_slot, attr_value in self.attrs['MagicAttrs'].items():
            # 计算精炼值并加回该字段本身
            # 注意精炼为round
            # 加到精炼镶嵌特殊属性中
            if attr_slot in self.changed_attrs:
                self.changed_attrs['MagicAttrs'][attr_slot] += int(attr_value * refine[self.strength] + 0.5)
            else:
                self.changed_attrs['MagicAttrs'][attr_slot] = int(attr_value * refine[self.strength] + 0.5)


        # 镶嵌
        if self.embedding is not None:
            plug = [0, 0.195, 0.39, 0.585, 0.78, 0.975, 1.17, 1.755, 2.6]
            if len(self.embedding) < len(self.data[5]):
                # 实际镶嵌数量大于预计，说明装备存在更迭
                raise AttributeError("装备镶嵌孔数量有改变！")
            else:

                # luatable必须用index的方式迭代
                for index in range(1, len(self.embedding) + 1):
                    # 对于每一个镶嵌孔，先取出五行石等级
                    embedding_lv = self.embedding[f"embedding_{index}"]
                    # 再取出对应属性字段及数值
                    _attr = self.equip_data[f"_DiamondAttributeID{index}"]
                    # 计算最终属性
                    # 注意镶嵌为向下取整
                    if _attr[0] not in self.changed_attrs['MagicAttrs']:
                        self.changed_attrs['MagicAttrs'][_attr[0]] = int(max(int(_attr[1]), int(_attr[2])) * plug[embedding_lv])
                    else:
                        self.changed_attrs['MagicAttrs'][_attr[0]] += int(max(int(_attr[1]), int(_attr[2])) * plug[embedding_lv])

        # 小附魔
        if self.enhance is not None:
            # 读取小附魔id
            enhance_id = self.data[6]
            try:
                # 取出对应小附魔数据
                enhance_data = enchant['enhance'][enhance_id]
                # 记录小附魔名称
                self.enhance = enhance_data['AttriName'][:-1]
                self.enhance_name = enhance_data['Name']
                # 添加小附魔属性
                if enhance_data["Attribute1ID"] not in self.changed_attrs['MagicAttrs']:
                    self.changed_attrs['MagicAttrs'][enhance_data["Attribute1ID"]] = max(
                        int(enhance_data['Attribute1Value1']), int(enhance_data['Attribute1Value2']))
                else:
                    self.changed_attrs['MagicAttrs'][enhance_data["Attribute1ID"]] += max(
                        int(enhance_data['Attribute1Value1']), int(enhance_data['Attribute1Value2']))
            except KeyError as e:
                print(f"KeyError: {e} at Scripts/ReadData/Equips/equip_type.py enhance: 无小附魔")
                self.enhance = "无小附魔"

        # 大附魔
        # 读取到大附魔信息
        if self.enchant is not None:
            enchant_id = self.data[7]
            try:
                # 取出对应附魔数据
                enchant_data = enchant['enchant'][enchant_id]
                self.enchant: str = enchant_data['Name']
                # 伤帽
                if enchant_data['UIID'] == "帽子限时" and self.enchant.endswith("·伤·帽"):
                    # 属性名：基础外功破防等级
                    _attr_slot = "atPhysicsOvercomeBase"
                    # 属性值: 从描述中查找
                    _attr_value = int([i.group("value") for i in
                                       compile(r'则破防等级提高(?P<value>.+?)点').finditer(enchant_data["_AttriName"])][
                                          0])
                    # 添加到装备属性中
                    if _attr_slot not in self.changed_attrs['MagicAttrs']:
                        self.changed_attrs['MagicAttrs'][_attr_slot] = _attr_value
                    else:
                        self.changed_attrs['MagicAttrs'][_attr_slot] += _attr_value
                # 伤衣
                if enchant_data['UIID'] == "上装限时" and self.enchant.endswith("·伤·衣"):
                    # 属性名：基础外功攻击
                    _attr_slot = "atPhysicsAttackPowerBase"
                    # 属性值: 从描述中查找
                    _attr_value = int([i.group("value") for i in
                                       compile(r"外功提高(?P<value>.+?)点").finditer(enchant_data["_AttriName"])][0])
                    # 添加到装备属性中
                    if _attr_slot not in self.changed_attrs['MagicAttrs']:
                        self.changed_attrs['MagicAttrs'][_attr_slot] = _attr_value
                    else:
                        self.changed_attrs['MagicAttrs'][_attr_slot] += _attr_value

            except KeyError as e:
                print(f"KeyError: {e} at Scripts/ReadData/Equips/equip_type.py enchant: 无大附魔")
                self.enchant = "无大附魔"

    def __str__(self) -> str:
        return f'''
        {self.__class__}:
            id: {self.id}
            name:{self.name}
            level:{self.level}
            embedding:{self.embedding}
            enhance:{self.enhance}
            enchant:{self.enchant}
            stone:{self.stone}
            Attrs:{self.attrs}
    '''


class HAT(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
            'embedding_2': None,
        }
        self.enhance = ''
        self.enchant = ''

        self.subtype = 'armor'


class JACKET(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
            'embedding_2': None,
        }
        self.enhance = ''
        self.enchant = ''

        self.subtype = 'armor'


class BELT(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
            'embedding_2': None,
        }
        self.enhance = ''
        self.enchant = ''

        self.subtype = 'armor'


class WRIST(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
            'embedding_2': None,
        }
        self.enhance = ''
        self.enchant = ''

        self.subtype = 'armor'


class BOTTOMS(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
            'embedding_2': None,
        }
        self.enhance = ''
        self.enchant = ''

        self.subtype = 'armor'


class SHOES(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
            'embedding_2': None,
        }
        self.enhance = ''
        self.enchant = ''

        self.subtype = 'armor'


class NECKLACE(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
        }
        self.enhance = ''

        self.subtype = 'trinket'


class PENDANT(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
        }
        self.enhance = ''

        self.subtype = 'trinket'


class RING_1(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.enhance = ''

        self.subtype = 'trinket'


class RING_2(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.enhance = ''

        self.subtype = 'trinket'


class PRIMARY_WEAPON(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
            'embedding_2': None,
            'embedding_3': None,
        }
        self.enhance = ''
        self.stone = ''

        self.subtype = 'weapon'


class SECONDARY_WEAPON(_Equip):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.embedding = {
            'embedding_1': None,
        }
        self.enhance = ''

        self.subtype = 'weapon'


position_mapping = {
    2: SECONDARY_WEAPON,
    3: JACKET,
    4: HAT,
    5: NECKLACE,
    6: RING_1,
    7: RING_2,
    8: BELT,
    9: PENDANT,
    10: BOTTOMS,
    11: SHOES,
    12: WRIST,
    0: PRIMARY_WEAPON
}
