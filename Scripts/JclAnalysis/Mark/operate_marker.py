# coding: utf-8
# author: LinXin
# 技能数+技能伤害：阵云结晦、月照连营、雁门迢递、绝国、绝刀、斩刀
# 技能数: 盾飞（作为最终权重）
# 技能伤害: 飞击飞压回击、流血

from typing import Dict, Union, Literal
from collections import namedtuple

from CustomClasses.TypeHints import Attribute
from .marker_const import HASTE_TO_GCD, STANDARD_OPERATE, SKILL_TO_GCD_INDEX, CHENGWU, USED_SKILL_DATA


advance_buff = namedtuple('作用于技能的增益buff', ['DaoHun', 'XueNu', 'CongRong', 'YuJian', 'FenYe'])


class OperateMarker:

    def __init__(self):
        # 基础设置
        self._BASIC_SETTING = {
            '分山劲玉简': False,
            '伤腰': False,
            '橙武': False,
            '套装技能': False
        }
        # 玩家属性
        self._player_attribute = {
            'PhysicsAttackPowerBase': 0,
            'PhysicsAttackPower': 0,
            'MeleeWeaponDamage': 0,
        }
        # 标准循环技能增益情况
        self._standard_skill_advance = None
        # 标准循环各技能伤害
        self._standard_skill_damage_result = {'云': 0, '月': 0, '雁': 0, '斩': 0, '绝': 0}
        # 标准循环各技能数量
        self._standard_skill_count_result = {'云': 0, '月': 0, '雁': 0, '斩': 0, '绝': 0}
        # 实际循环各技能伤害
        self._real_skill_damage_result = {'云': 0, '月': 0, '雁': 0, '斩': 0, '绝': 0}
        # 实际循环各技能数量
        self._real_skill_count_result = {'云': 0, '月': 0, '雁': 0, '斩': 0, '绝': 0}
        # 玩家属性类
        # noinspection PyTypeChecker
        self._player_equip_data: Attribute = None
        # 玩家操作分析数据
        self._player_operate_data = None
        # 玩家奇穴
        self._player_talent = None
        # 战斗时间
        self._fight_time = 0


    def basic_setting(self, player_equip_data: Attribute, fight_time: int):
        """
        面板属性\n
        云山经附魔，伤腰，橙武，套装技能\n
        通过配置计算出标准情况的各技能buff\n
        :return:
        """
        self._player_equip_data = player_equip_data
        self._fight_time = fight_time
        # 1. 提取出需要的属性
        try:
            _json_attrib = eval(player_equip_data.json_attributes)
        except TypeError as e:
            print(f"TypeError: {e} at Scripts/JclAnalysis/Mark/operate_marker.py basic_setting: 未知错误!")
            return
        self._player_attribute['PhysicsAttackPowerBase'] = _json_attrib['PhysicsAttackPowerBase']
        self._player_attribute['PhysicsAttackPower'] = _json_attrib['PhysicsAttackPower'] - _json_attrib['PhysicsAttackPowerBase']
        self._player_attribute['MeleeWeaponDamage'] = _json_attrib['MeleeWeaponDamage'] + _json_attrib['MeleeWeaponDamageRand'] // 2
        # 2, 云山经附魔
        self._BASIC_SETTING['分山劲玉简'] = player_equip_data.yunshan_enchant
        # 3. 伤腰, 橙武
        self._BASIC_SETTING['伤腰'] = player_equip_data.belt_enchant
        _name: str = player_equip_data.equip['PRIMARY_WEAPON'].name
        _name = _name[:_name.find('(')]
        if _name in CHENGWU['分山劲']:
            self._BASIC_SETTING['橙武'] = True
        # 4. 套装
        skill_set_effect = {1932, 1933}
        if isinstance(player_equip_data.equip_set_count, dict):
            for set_data in player_equip_data.equip_set_count.values():
                for position in {'2_1', '2_2', '4_1', '4_2'}:
                    _checked = False    # 是否在当前字段内查找到了对应的id
                    if position in set_data['attrs']:
                        _data = set_data['attrs'][position]
                        if _data is not None:
                            if max(int(_data['attr'][1]), int(_data['attr'][2])) in skill_set_effect:
                                _checked = True
                                break
                if _checked:
                    if set_data['count'] >= int(position[0]):
                        self._BASIC_SETTING['套装技能'] = True
        # print(self._BASIC_SETTING)
        # 5. 计算标准情况buff覆盖
        self._player_talent = player_equip_data.player_talent
        _yujian = 1 if self._BASIC_SETTING['分山劲玉简'] else 0
        _daohun = 1 if '刀魂' in self._player_talent else 0
        _fenye = 1 if '分野' in self._player_talent else 0
        _congrong = 1 if '从容' in self._player_talent else 0

        if not self._BASIC_SETTING['橙武']:
            self._standard_skill_advance = {
                # 技能数+技能伤害：阵云结晦、月照连营、雁门迢递、绝国、绝刀、斩刀
                # ['DaoHun', 'XueNu', 'CongRong', 'YuJian', 'FenYe']
                '云': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 6*_yujian, 1*_fenye),
                '月': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 6*_yujian, 1*_fenye),
                '雁': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 6*_yujian, 1*_fenye),
                '斩': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 5.64*_yujian, 1*_fenye),
                '绝': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 3.95*_yujian, 1*_fenye),
            }
        else:
            self._standard_skill_advance = {
                # 技能数+技能伤害：阵云结晦、月照连营、雁门迢递、绝国、绝刀、斩刀
                # ['DaoHun', 'XueNu', 'CongRong', 'YuJian', 'FenYe']
                '云': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 6*_yujian, 1*_fenye),
                '月': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 6*_yujian, 1*_fenye),
                '雁': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 6*_yujian, 1*_fenye),
                '斩': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 5.64*_yujian, 1*_fenye),
                '绝': advance_buff(1*_daohun, 50/fight_time+2, 1*_congrong, 3.51*_yujian, 1*_fenye),
            }

    def run(self, player_operate_data):
        self._player_operate_data = player_operate_data
        self._get_standard_skill_count(self._fight_time)
        self._get_standard_skill_damage()
        self._get_real_skill_count_and_damage()

        return (
            self._standard_skill_count_result,
            self._standard_skill_damage_result,
            self._real_skill_count_result,
            self._real_skill_damage_result
        )

    def _get_damage_by_buff(self, skill: Literal['云', '月', '雁', '斩', '绝'], buff: advance_buff):
        """
        获取理论技能伤害\n
        :param buff: ('DaoHun', 'XueNu', 'CongRong', 'YuJian', 'FenYe')
        :return:
        """
        # assert self._player_equip_data is None, "Scripts/JclAnalysis/Mark/operate_marker.py _get_damage_by_buff： 未知初始化错误"
        _fenhen = 1 if '愤恨' in self._player_talent else 0
        _skill_data = USED_SKILL_DATA[skill]
        _AttackPowerPercentAdd = 0
        _AllDamagePercentAdd = 0
        # 奇穴部分
        # 刀魂
        _AttackPowerPercentAdd += buff.DaoHun * (153 / 1024)
        # 血怒
        if _fenhen:
            _AttackPowerPercentAdd += buff.XueNu * (133 / 1024)
        else:
            _AttackPowerPercentAdd += buff.XueNu * (102 / 1024)
        # 从容
        _AttackPowerPercentAdd += buff.CongRong * (204 / 1024)
        # 玉简
        _AllDamagePercentAdd += buff.YuJian * (31 / 1024)
        # 分野
        _AllDamagePercentAdd += buff.FenYe * (51 / 1024)
        # 装备部分
        # 橙武
        if skill == '斩' and self._BASIC_SETTING['橙武']:
            _AllDamagePercentAdd += 51 / 1024
        # 套装
        # 不计算盾压劫刀
        # 秘籍
        _AllDamagePercentAdd += _skill_data.RecipeRate
        # 绝刀怒气  120再改
        if skill == '绝':
            if '吓魂' in self._player_talent:
                _AllDamagePercentAdd += 0.8
            else:
                _AllDamagePercentAdd += 0.8
        # 伤腰
        if self._BASIC_SETTING['伤腰']:
            _AllDamagePercentAdd += 0.0093
        # 非侠士
        _npc_advance = 174 / 1024
        if skill in {'云', '月', '雁'}:
            _npc_advance += 614 / 1024

        # 计算伤害
        # 攻击
        _attack = self._player_attribute['PhysicsAttackPowerBase'] * (1 + _AttackPowerPercentAdd) + self._player_attribute['PhysicsAttackPower']
        _weapon = self._player_attribute['MeleeWeaponDamage']
        # 伤害
        _damage = int((_attack * _skill_data.AttackRate + _skill_data.BaseDamage + _weapon * _skill_data.WeaponRate) * (1 + _AllDamagePercentAdd) * (1 + _npc_advance))
        print(f"{skill}: {_damage}, {_AttackPowerPercentAdd}, {_AllDamagePercentAdd}")
        return _damage

    def _get_standard_skill_count(self, fight_time: int) -> Dict[str, int]:
        """
        获取理论技能数\n
        20220911: cw默认二段，非cw默认一段\n
        :return:
        """
        # 江湖无限赛季加速数值
        if self._BASIC_SETTING['橙武']:
            _gcd = HASTE_TO_GCD[1928]
            _standard_operate = STANDARD_OPERATE['橙武']
        else:
            _gcd = HASTE_TO_GCD[43]
            _standard_operate = STANDARD_OPERATE['非橙武']
        # 通过循环框架计算每个循环耗时
        _standard_time = 0
        _standard_skills = {}
        # 斩刀cd计算
        _cd_zhandao = 0
        try:
            # 先计算起手
            for skill in _standard_operate['header']:
                if skill in _standard_skills:
                    _standard_skills[skill] += 1
                else:
                    _standard_skills[skill] = 1
                current_gcd = _gcd[SKILL_TO_GCD_INDEX[skill]]
                _standard_time += current_gcd
                # 斩刀cd计算
                if skill == '斩':
                    _standard_time += _cd_zhandao
                    _cd_zhandao = 10 - current_gcd
                else:
                    _cd_zhandao = max(0, _cd_zhandao - current_gcd)

                if _standard_time >= fight_time:
                    break
            # 计算固定循环部分
            while _standard_time < fight_time:
                for skill in _standard_operate['body']:
                    if skill in _standard_skills:
                        _standard_skills[skill] += 1
                    else:
                        _standard_skills[skill] = 1
                    current_gcd = _gcd[SKILL_TO_GCD_INDEX[skill]]
                    _standard_time += current_gcd
                    # 斩刀cd计算
                    if skill == '斩':
                        _standard_time += _cd_zhandao
                        _cd_zhandao = 10 - current_gcd
                    else:
                        _cd_zhandao = max(0, _cd_zhandao - current_gcd)

                    if _standard_time >= fight_time:
                        break

        except KeyError as e:
            print(f"KeyError: {e} at Scripts/JclAnalysis/Mark/standard_operate.py get_standard_skill_count: 未知技能")
        finally:
            # 设置循环技能数
            for skill in _standard_skills:
                if skill in self._standard_skill_count_result:
                    self._standard_skill_count_result[skill] = _standard_skills[skill]
            return _standard_skills

    def _get_standard_skill_damage(self):
        for skill, standard_buff_data in self._standard_skill_advance.items():
            self._standard_skill_damage_result[skill] = self._get_damage_by_buff(skill, standard_buff_data)

    def _get_real_skill_count_and_damage(self):
        """
        读取实际技能数\n
        :return:
        """
        _analysis = self._player_operate_data['analysis']
        name_to_short_name = {
            '阵云结晦': '云', '月照连营': '月', '雁门迢递': '雁', '斩刀': '斩', '绝刀': '绝'
        }
        _count = {
            '阵云结晦': 0, '月照连营': 0, '雁门迢递': 0, '斩刀': 0, '绝刀': 0
        }
        for skill, skill_data in _analysis.items():
            if skill in name_to_short_name:
                skill = name_to_short_name[skill]
                _buffs = skill_data['Buffs']
                # noinspection PyTypeChecker
                self._real_skill_damage_result[skill] = self._get_damage_by_buff(skill,
                    advance_buff(_buffs['DaoHun'], _buffs['XueNu'], _buffs['CongRong'], _buffs['YuJian'], _buffs['FenYe']))

        for _, data in self._player_operate_data['operate_list'].items():
            if data['name'] in _count:
                _count[data['name']] += 1

        for skill, count in _count.items():
            skill = name_to_short_name[skill]
            self._real_skill_count_result[skill] = count


























