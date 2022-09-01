"""
计算总属性的类, 因多处位置都需要调用属性计算
"""
from CustomClasses.TypeHints import PlayerEquip, Equip
from Sources.Jx3_Datas.Files.jx3_stone import AttribTypeToAttribSlot
from Sources.Jx3_Datas.Files.jcl_data import slot_to_name_dictionary


from typing import Any
from json import dumps
import re


class Attribute:

    def __init__(self, equip: PlayerEquip):
        self.equip = equip
        # 导入装备类

        # 合计属性
        self._attributes = None
        # json格式
        self.json_attributes = None
        # 合计套装
        self._equip_set_count = None
        # 合计镶嵌 {数量，总等级}
        self.embedding_count = {'quantity': 0, 'total_level': 0}
        # 玩家心法
        self.player_kungfu = None
        # 玩家奇穴
        # 在reader_main._get_player_info中被传入
        self.player_talent = None
        # 玉简附魔
        # self._yunshan_enchant = None

        # 装备名
        self._EQUIP_NAME = ["HAT", "JACKET", "BELT", "WRIST", "BOTTOMS", "SHOES", "NECKLACE", "PENDANT", "RING_1",
                            "RING_2", "PRIMARY_WEAPON", "SECONDARY_WEAPON"]
        # 套装名称映射
        self._SET_MAPPING = {"T套": "门派套装", "切糕": "切糕套装", "御厨套装": "冬至套装"}

    # def set_equip_object(self, equip: PlayerEquip):
    #     """
    #     外部传入PlayerEquip Object用
    #     :param equip:
    #     :return:
    #     """
    #     self.equip = equip

    def __str__(self):
        print(*["{}: {}\n".format(slot_to_name_dictionary[k], v) for k, v in self._attributes.items()])
        return ""

    def __getitem__(self, item):
        if item in self._attributes:
            return self._attributes[item]
        return "0"

    @property
    def yunshan_enchant(self) -> bool:
        _bottom = self.equip['BOTTOM']
        if _bottom is not None:
            if _bottom.enchant is not None and '玉简' in _bottom.enchant:
                return True
        return False

    def calc_attribute(self):
        """
        用于计算属性的核心函数
        :return:
        """
        # 1. 遍历每件装备
        # 1.1 将该装备属性加到总属性中
        #   _Equip.attrs
        # 1.2 将该装备套装数据加至总套装计数中,
        #   >1 门派套装
        #       1.1 BelongSchool=苍云
        #       1.2 MagicKind=外功/防御
        #       1.3 _SetAttrbs.Name=xxxxT套
        #   >2 切糕
        #       2.1 GetType=生活技能
        #       2.2 MagicKind=身法/防御
        #       2.3 _SetAttrbs.Name=xxxx切糕
        #   >3 冬至
        #       3.1 GetType=活动
        #       3.2 BelongSchool=苍云
        #       3.3 MagicKind=外功/防御
        #       3.4 _SetAttrbs.Name=xxxx品御厨套装
        # 1.3 将该装备镶嵌情况加至总镶嵌计数中
        #   _Equip.embedding
        # 清空属性
        self._attributes = {}
        self._equip_set_count = {}
        self.embedding_count = {'quantity': 0, 'total_level': 0}
        # 1. 遍历每件装备
        for equip_name in self._EQUIP_NAME:
            # 过滤掉该部位未穿装备的情况
            if self.equip[equip_name] is None:
                continue
            # 先读取精炼镶嵌
            self.equip[equip_name].read_embedding_and_strength()
            #
            self._for_everything_in_each_equip(self.equip[equip_name])
        # 2. 计算套装属性
        # 3. 计算五彩石属性
        self._for_set_and_stone_attribute()
        # 4. 计算心法固定增益属性（不包括额外主属性转化）
        self._for_mount_basic_attribute()
        # ---------以下需要合并后的属性---------
        # 5. 计算奇穴提供的属性增益
        self._for_percent_add_attribute_from_talent()
        # 6. 汇总并计算基础属性
        self._sum_and_calc_base_attributes()
        # 7. 计算身法/力道系统转化属性
        self._for_base_potential_to_other_by_system()
        # 8. 计算属性的非基础增益(奇穴)
        self._for_final_percent_add_from_talent()
        # 9. 计算心法额外主属性转化
        self._for_mount_final_attribute()

        # 将部分属性转化为百分比
        # 生成可导出的json格式属性
        self._attrib_value_to_attrib_final()
        # 测试用

        # 调试用
        print("Scripts/ReadData/Equips/attribute_calc.py attributes")
        print(self)
        print(self.json_attributes)
        # print("Scripts/ReadData/Equips/equip_reader.py equip_set_count " + self.equip_set_count.__repr__())
        # print("Scripts/ReadData/Equips/equip_reader.py embedding_count " + self.embedding_count.__repr__())







    def _for_everything_in_each_equip(self, equip_obj: Equip) -> Any:
        """
        执行calc_attribute的第一步，计算装备属性、套装和镶嵌
        :param equip_obj:
        :return:
        """
        # 1. 属性计算
        _equip_attrs = equip_obj.attrs
        # 基础属性
        for attrib_value in _equip_attrs.values():
            for slot, value in attrib_value.items():
                if slot in self._attributes:
                    self._attributes[slot] += value
                else:
                    self._attributes[slot] = value

        # 精炼镶嵌属性
        _equip_special_attrs = equip_obj.changed_attrs
        # print(_equip_special_attrs)
        # 基础属性
        for attrib_value in _equip_special_attrs.values():
            for slot, value in attrib_value.items():
                if slot in self._attributes:
                    self._attributes[slot] += value
                else:
                    self._attributes[slot] = value

        # 2. 套装计算
        # 套装数量计算
        _equip_data = equip_obj.equip_data
        try:
            _set_attribs_name = _equip_data['_SetAttrbs']['Name']
            # 在存在SetAttrib的情况下再向下判断
            # 判断是否可触发套装
            if _equip_data['BelongSchool'] in {"苍云", "通用"}:
                # 判断套装类型
                for set_type_symbol in self._SET_MAPPING:
                    if set_type_symbol in _set_attribs_name:
                        # 套装名称
                        set_key = f"{self._SET_MAPPING[set_type_symbol]}_{_equip_data['MagicKind']}_{_equip_data['Level']}"
                        # 记录套装
                        self._add_set_data_to_set_count(set_key=set_key, equip_data=_equip_data)
                        break

        except KeyError as e:
            print(f"KeyError: {e} at Scripts/ReadData/Equips/equip_reader.py _for_everything_in_equip: 该装备不属于套装")
        except TypeError as e:
            print(f"TypeError: {e} at Scripts/ReadData/Equips/equip_reader.py _for_everything_in_equip: 该装备不属于套装")

        # 3. 镶嵌统计
        if equip_obj.embedding is not None:
            for value in equip_obj.embedding.values():
                if value is not None:
                    self.embedding_count['quantity'] += 1
                    self.embedding_count['total_level'] += value

    def _for_set_and_stone_attribute(self) -> Any:
        """
        执行calc_attribute的第2,3步, 计算套装属性和五彩石属性
        :return:
        """
        # 1. 套装属性
        for set_type, set_info in self._equip_set_count.items():
            # 套装最少有两件
            if set_info['count'] > 1:
                for set_count in range(2, set_info['count'] + 1):
                    for i in range(1, 3):
                        # 生成x_y的键名
                        attr_info = set_info['attrs'][f"{set_count}_{i}"]
                        if attr_info is not None:
                            attr_info = attr_info['attr']
                            if attr_info[0] in self._attributes:
                                self._attributes[attr_info[0]] += max(int(attr_info[1]), int(attr_info[2]))
                            else:
                                self._attributes[attr_info[0]] = max(int(attr_info[1]), int(attr_info[2]))
                            # 这里还需要记录简略套装信息

        # 2. 五彩石属性
        # 依次取出词条
        if self.equip['PRIMARY_WEAPON'].stone['data'] is not None:
            for stone_attrib in self.equip['PRIMARY_WEAPON'].stone['data']:
                # 判断是否满足激活五彩石的条件
                if self.embedding_count['quantity'] >= int(stone_attrib[4]) and self.embedding_count['total_level'] >= int(stone_attrib[5]):
                    # 翻译对应属性字段
                    attr_slot = AttribTypeToAttribSlot(stone_attrib[1], stone_attrib[2])
                    attr_value = int(float(stone_attrib[3]))
                    # 添加至总属性中
                    if attr_slot in self._attributes:
                        self._attributes[attr_slot] += attr_value
                    else:
                        self._attributes[attr_slot] = attr_value

    def _for_mount_basic_attribute(self) -> Any:
        """
        执行calc_attribute的第4步，添加心法固定属性
        :return:
        """
        mount_attribs = {
            '分山劲': {
                'atPhysicsAttackPowerBase': 1526,
                'atPhysicsOvercomeBase': 694,
                'atVitalityBase': 38,
                'atAgilityBase': 38,
                'atStrengthBase': 37,
                'atParryBase': 554,
                'atPhysicsShieldBase': 400,
                'atMagicShield': 400,
            },
            '铁骨衣': {
                'atVitalityBase': 38,
                'atAgilityBase': 38,
                'atStrengthBase': 37,
                'atParryBase': 914,
                'atParryValueBase': 2114,
                'atPhysicsShieldBase': 948,
                'atMagicShield': 400,
            }
        }
        if self.player_kungfu not in mount_attribs:
            raise
        for slot, value in mount_attribs[self.player_kungfu].items():
            if slot not in self._attributes:
                self._attributes[slot] = value
            else:
                self._attributes[slot] += value

    def _for_percent_add_attribute_from_talent(self) -> Any:
        """
        执行第5步, 读取奇穴并添加对应属性
        :return:
        """
        # 奇穴到属性值的映射
        talent_add_mapping: dict[str: dict] = {
            "活脉": {"atVitalityBasePercentAdd": 102, "atAgilityBasePercentAdd": 102},
            "活血": {"atVitalityBasePercentAdd": 102},
            "用御": {"atHasteBasePercentAdd": 102},
            "从容": {"atPhysicsAttackPowerPercent": 205},
        }
        if self.player_talent is not None:
            for talent in talent_add_mapping:
                if talent in self.player_talent:
                    # 添加对应属性
                    for slot, value in talent_add_mapping[talent].items():
                        if slot in self._attributes:
                            self._attributes[slot] += value
                        else:
                            self._attributes[slot] = value

    def _sum_and_calc_base_attributes(self) -> Any:
        """
        执行第6步，先行汇总并计算属性
        :return:
        """
        for slot in self._attributes:
            if 'atAllType' in slot:
                # 全属性类型
                new_slot = slot.replace("AllType", "Physics")
                if new_slot in self._attributes:
                    self._attributes[new_slot] = self._attributes[slot]
            elif 'BasePotentialAdd' in slot:
                # 全主属性
                value = self._attributes[slot]
                for new_slot in ['atVitalityBase', 'atAgilityBase', 'atStrengthBase']:
                    self._attributes[new_slot] += value
            elif 'BasePercentAdd' in slot:
                # 主属性加成
                slot_name = \
                [match.group('attrtype') for match in re.compile(r'at(?P<attrtype>.+?)BasePercentAdd').finditer(slot)][
                    0]
                # 这一步只能加成主属性
                if slot_name in ['Vitality', 'Agility', 'Strength', 'Spunk', 'Spirit']:
                    new_slot = f"at{slot_name}Base"
                    value = self._attributes[slot]
                    if new_slot in self._attributes:
                        self._attributes[new_slot] += int(self._attributes[new_slot] * (value / 1024))
        if 'atPhysicsShieldAdditional' in self._attributes:
            self._attributes['atPhysicsShieldBase'] += self._attributes['atPhysicsShieldAdditional']

    def _for_base_potential_to_other_by_system(self) -> Any:
        """
        执行calc_attribute中的第7步，主属性系统通用转化
        :return:
        """
        # 这里的值为其准确的小数值再向下取整
        # 身法
        # 对会心加成
        if 'atPhysicsCriticalStrike' in self._attributes:
            self._attributes['atPhysicsCriticalStrike'] += int(self._attributes['atAgilityBase'] * 0.64)
        else:
            self._attributes['atPhysicsCriticalStrike'] = int(self._attributes['atAgilityBase'] * 0.64)
        # 力道
        # 对攻击加成
        self._attributes['atPhysicsAttackPowerBase'] += int(self._attributes['atStrengthBase'] * 0.15)
        # 对破防加成
        if 'atPhysicsOvercomeBase' in self._attributes:
            self._attributes['atPhysicsOvercomeBase'] += int(self._attributes['atStrengthBase'] * 0.3)
        else:
            self._attributes['atPhysicsOvercomeBase'] = int(self._attributes['atStrengthBase'] * 0.3)

    def _for_final_percent_add_from_talent(self) -> Any:
        """
        执行第8步，奇穴中的最终属性转化（从容、用御）
        :return:
        """
        if 'atPhysicsAttackPowerPercent' in self._attributes:
            self._attributes['atPhysicsAttackPower'] = int(self._attributes['atPhysicsAttackPowerBase'] * (
                    self._attributes['atPhysicsAttackPowerPercent'] / 1024))

    def _for_mount_final_attribute(self) -> Any:
        """
        执行第9步, 计算心法提供的主属性转化
        :return:
        """
        # 分山劲
        if self.player_kungfu == '分山劲':
            # 1.71攻击
            if 'atPhysicsAttackPower' in self._attributes:
                self._attributes['atPhysicsAttackPower'] += int(self._attributes['atAgilityBase'] * (1751 / 1024))
            else:
                self._attributes['atPhysicsAttackPower'] = int(self._attributes['atAgilityBase'] * (1751 / 1024))
            # 0.1招架
            self._attributes['atParryBase'] += int(self._attributes['atAgilityBase'] * (102 / 1024))
            # 1拆招值
            if 'atParryValueBase' in self._attributes:
                self._attributes['atParryValueBase'] += self._attributes['atAgilityBase'] * 1
            else:
                self._attributes['atParryValueBase'] = self._attributes['atAgilityBase'] * 1
        elif self.player_kungfu == '铁骨衣':
            # 0.15招架
            self._attributes['atParryBase'] += int(self._attributes['atVitalityBase'] * (154 / 1024))
            # 0.5拆招
            self._attributes['atParryValueBase'] += int(self._attributes['atVitalityBase'] * (512 / 1024))
            # 0.04攻击
            if 'atPhysicsAttackPower' in self._attributes:
                self._attributes['atPhysicsAttackPower'] += int(self._attributes['atVitalityBase'] * (41 / 1024))
            else:
                self._attributes['atPhysicsAttackPower'] = int(self._attributes['atVitalityBase'] * (41 / 1024))

    def _add_set_data_to_set_count(self, *, set_key: str, equip_data: dict) -> Any:
        """
        将套装装备信息加入套装统计数据中
        :param set_key:
        :param equip_data:
        :return:
        """
        try:
            if set_key not in self._equip_set_count:
                self._equip_set_count[set_key] = {
                    "count": 1,
                    "level": int(equip_data['Level']),
                    "attrs": equip_data['_SetData']
                }
            else:
                self._equip_set_count[set_key]['count'] += 1

        except KeyError as e:
            print(f"KeyError: {e} at Scripts/ReadData/Equips/equip_reader.py _add_set_data_to_set_count")

    def _attrib_value_to_attrib_final(self) -> Any:
        """
        将属性数据转化为最终输出的数据格式
        :return:
        """
        json_data = {"Vitality": 0, "Agility": 0, "Spirit": 0, "Spunk": 0, "Strength": 0, "PhysicsAttackPowerBase": 0,
                     "PhysicsAttackPower": 0, "PhysicsCriticalStrikeRate": 0.0,
                     "PhysicsCriticalDamagePowerPercent": 0, "PhysicsOvercomePercent": 0, "StrainPercent": 0,
                     "HastePercent": 0, "SurplusValue": 0, "MaxHealth": 0,
                     "PhysicsShieldPercent": 0, "LunarShieldPercent": 0,
                     "ToughnessDefCriticalPercent": 0, "DecriticalDamagePercent": 0, "DodgePercent": 0, "ParryPercent": 0,
                     "ParryValue": 0, "ActiveThreatCoefficient": 0, "MeleeWeaponAttackSpeed": 0, "MeleeWeaponDamage": 0, "MeleeWeaponDamageRand": 0}

        # 体质, 身法, 力道, 基础攻击, 破招, 拆招值, 武器系列
        numeric_attr_mapping = {
            "Vitality": "atVitalityBase",
            "Agility": "atAgilityBase",
            "Strength": "atStrengthBase",
            "PhysicsAttackPowerBase": "atPhysicsAttackPowerBase",
            "SurplusValue": "atSurplusValueBase",
            "ParryValue": "atParryValueBase",
            "MeleeWeaponAttackSpeed": "atMeleeWeaponAttackSpeedBase",
            "MeleeWeaponDamage": "atMeleeWeaponDamageBase",
            "MeleeWeaponDamageRand": "atMeleeWeaponDamageRand"
        }
        percentage_attr_mapping = {
            "PhysicsCriticalStrikeRate": ("atPhysicsCriticalStrike", 35737.5),
            "PhysicsCriticalDamagePowerPercent": ("atPhysicsCriticalDamagePowerBase", 12506.25),
            "PhysicsOvercomePercent": ("atPhysicsOvercomeBase", 35737.5),
            "StrainPercent": ("atStrainBase", 34458.75),
            "ToughnessDefCriticalPercent": ("atToughnessBase", 35737.5)
        }
        non_linear_percentage_mapping = {
            "PhysicsShieldPercent": ("atPhysicsShieldBase", 19091.25),
            "LunarShieldPercent": ("atMagicShield", 19091.25),
            "ParryPercent": ("atParryBase", 16293.75),
            "DodgePercent": ("atDodge", 17355),
        }
        for slot in numeric_attr_mapping:
            if numeric_attr_mapping[slot] in self._attributes:
                json_data[slot] = self._attributes[numeric_attr_mapping[slot]]
        # 最终攻击
        json_data["PhysicsAttackPower"] = self._attributes['atPhysicsAttackPower'] + self._attributes['atPhysicsAttackPowerBase']
        # 线性百分比属性：会心，会效，破防，无双, 御劲
        for slot in percentage_attr_mapping:
            if percentage_attr_mapping[slot][0] in self._attributes:
                json_data[slot] = self._attributes[percentage_attr_mapping[slot][0]] / percentage_attr_mapping[slot][1]
            if slot == 'PhysicsCriticalDamagePowerPercent':
                json_data[slot] = min(3, 1.75 + json_data[slot])
        # 加速
        if 'atHasteBase' in self._attributes:
            _haste_add = 0
            if 'atHasteBasePercentAdd' in self._attributes:
                _haste_add = self._attributes['atHasteBasePercentAdd']
            json_data["HastePercent"] = min(0.25, (self._attributes['atHasteBase'] / 43856.25) + (_haste_add / 1024))
        # 非线性百分比属性：外防，内防，招架, 闪避
        for slot in non_linear_percentage_mapping:
            if non_linear_percentage_mapping[slot][0] in self._attributes:
                _value = self._attributes[non_linear_percentage_mapping[slot][0]]
                json_data[slot] = _value / (_value + non_linear_percentage_mapping[slot][1])
            # 不同属性特殊处理
            if slot in {"PhysicsShieldPercent", "LunarShieldPercent"}:
                json_data[slot] = min(0.75, json_data[slot])
            elif slot == "ParryPercent":
                json_data[slot] += 0.03

        try:
            del self._attributes['atPhysicsAttackPowerPercent']
        except KeyError:
            pass
        try:
            del self._attributes['atSkillEventHandler']
        except KeyError:
            pass

        self.json_attributes = dumps(json_data)