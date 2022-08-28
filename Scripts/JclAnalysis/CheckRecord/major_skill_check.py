# coding: utf-8
# author: LinXin
# 主要技能的类型检查
# 分山: 阵云*3, 绝国, 斩刀, 绝刀, 盾击, 盾飞
# 铁骨: 盾刀, 盾击, 盾压, 流血, 斩刀, 绝刀, 劫刀, 断马

from typing import Dict

from CustomClasses.TypeHints import Attribute
from Scripts.Config.config import ConfigSetting
from Sources.Jx3_Datas.Files.jx3_skill import skill
from Sources.Jx3_Datas.Files.get_other_data import get_buff_or_skill_from_jx3box


class MajorSkillChecker:

    def __init__(self):
        self._major_skills_result = {}
        self._major_skills_list = {}
        self.config = ConfigSetting()

    @property
    def major_skill_list(self):
        return self._major_skills_list

    @property
    def major_skill_analysis(self):
        return self._major_skills_result

    def get_work_gen(self, kungfu: str) -> callable:
        """
        外层接口\n
        :return:
        """
        # 判断心法
        if kungfu == '分山劲':
            gen = self._check_fen_shan_skill()
        elif kungfu == '铁骨衣':
            # 盾刀, 盾击, 盾压, 流血, 斩刀, 绝刀, 劫刀, 断马
            pass
        gen.send(None)
        return gen

    def _check_fen_shan_skill(self):
        """
        检查分山技能: 阵云*3, 绝国, 斩刀, 绝刀, 盾击, 盾飞\n
        :return:
        """
        imports = {'阵云结晦', '月照连营', '雁门迢递', '绝国', '斩刀', '绝刀', '盾击', '盾飞'}
        player_skills = set()
        not_player_skills = set()
        zhenyun_max_layer = int(self.config['zhenyun_max_layer'])

        while True:
            # 获取数据
            msec, skill_id, skill_level, skill_name, buff_data = yield
            # 终止符
            if not skill_name:
                break
            # 针对重点技能的分析
            if skill_name in imports:
                buff_ret = self._checker_basic_buff(buff_data)
                match skill_name:
                    case '绝刀':
                        buff_ret['rage'] = 0
                        buff_ret['cw'] = False
                        buff_ret['ZhenYun_Overflow'] = False
                        # 绝刀怒气
                        if 9052 in buff_data:
                            # 存在绝刀怒气判定buff的情况
                            _lv = buff_data[9052][0]
                            if _lv > 4:
                                _lv = _lv - 4
                            buff_ret['rage'] = _lv
                        else:
                            # 绝刀速度太快导致不存在buff的情况
                            pass
                            # 暂无好的处理方案
                        # 橙武特效标记
                        if 8474 in buff_data:
                            buff_ret['cw'] = True
                        # 阵云溢出
                        if 22993 in buff_data:
                            if buff_data[22993][1] >= zhenyun_max_layer:
                                buff_ret['ZhenYun_Overflow'] = True
                if skill_name not in self._major_skills_result:
                    self._major_skills_result[skill_name] = {msec: buff_ret}
                else:
                    self._major_skills_result[skill_name][msec] = buff_ret
            # 技能轴
            if (skill_id, skill_level) not in not_player_skills:
                if (skill_id, skill_level) not in player_skills:
                    # 查询
                    try:
                        _kf = skill[skill_id][skill_level]['BelongKungfu']
                    except KeyError:
                        _kf = get_buff_or_skill_from_jx3box('skill', skill_id, skill_level)['BelongKungfu']
                    if _kf in {'10385', '10386', '10384', '10383', '10393', '24785'} and skill_name not in  {'盾飞', '阵云绝'}:
                        # 苍云套路+破招
                        player_skills.add((skill_id, skill_level))
                        self._major_skills_list[msec] = skill_name
                    else:
                        not_player_skills.add((skill_id, skill_level))
                else:
                    self._major_skills_list[msec] = skill_name










    @staticmethod
    def _checker_basic_buff(buff_data):
        ret = {
            'DaoHun': False,
            'FenYe': False,
            'CongRong': False,
            'FengMing': False,
            'ChongYun': False,
            'JunXiao': False,
            'Enchant_Hat': False,
            'XueNu_ly': 0,
            'LianZhan_ly': 0,
            'HanJia_ly': 0,
            'JianTie_ly': 0,
            'YuJian_ly': 0,
            'DunDang_lv': 0,
            'Enchant_Belt_lv': 0,
            }
        _ishave_mapping = {
            8627: 'DaoHun',
            17176: 'FenYe',
            8423: 'CongRong',
            14309: 'FengMing',
            14964: 'ChongYun',
            1428: 'JunXiao',
            15413: 'Enchant_Hat'
        }
        _islayer_mapping = {
            8244: 'XueNu_ly',
            8385: 'XueNu_ly',
            8386: 'XueNu_ly',
            8267: 'LianZhan_ly',
            8271: 'HanJia_ly',
            8272: 'JianTie_ly',
            21648: 'YuJian_ly'
        }
        _islevel_mapping = {
            8448: 'DunDang_lv',
            15455: 'Enchant_Belt_lv'
        }

        for _id, _key in _ishave_mapping.items():
            if _id in buff_data:
                ret[_key] = True
        for _id, _key in _islayer_mapping.items():
            if _id in buff_data:
                ret[_key] += buff_data[_id][1]
        for _id, _key in _islevel_mapping.items():
            if _id in buff_data:
                ret[_key] += buff_data[_id][0]

        # 大寒甲特殊处理
        if 17772 in buff_data:
            ret['HanJia_ly'] += buff_data[17772][1] * 100

        return ret
















