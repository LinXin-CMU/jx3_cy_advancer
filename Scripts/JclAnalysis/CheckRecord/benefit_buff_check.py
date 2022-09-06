# coding: utf-8
# author: LinXin
# 负责检查存在的增益
# 初始化时就需要传入数据，自动分析后直接调用数据结论

from typing import Dict

from Scripts.JclAnalysis.CheckRecord.benefic_buffs import BENEFIT_BUFFS, SELF_BUFFS


class BeneficialChecker:

    def __init__(self):
        # 增益数据
        self._BENEFIT_DATA = {}
        for buffs in BENEFIT_BUFFS.values():
            for idk, data in buffs.items():
                self._BENEFIT_DATA[idk] = data
        # 自身增益数据
        self._SELF_DATA = SELF_BUFFS
        # 增益ID
        self._BENEFIT_ID = [int(i.split('_')[0]) for i in self._BENEFIT_DATA.keys()]
        # 自身增益ID
        self._SELF_ID = [int(i.split('_')[0]) for i in self._SELF_DATA.keys()]
        # 最终数据
        self._other_benefit_buff_to_skill_data = {}
        self._self_benefit_buff_to_skill_data = {}

    @property
    def benefit_buffs(self):
        return self._other_benefit_buff_to_skill_data, self._self_benefit_buff_to_skill_data

    def check_benefit_buff(self, data):
        """
        将数据按buff重新统计分类\n
        :return:
        """
        self._other_benefit_buff_to_skill_data = {}
        self._self_benefit_buff_to_skill_data = {}
        for buff_id, _lvs in data.items():
            for buff_level, buff_data in _lvs.items():
                if buff_id in self._BENEFIT_ID or buff_id in self._SELF_ID:
                    key = f"{buff_id}_{buff_level}"
                    if key in self._BENEFIT_DATA:
                        # 添加进整合数据中
                        self._other_benefit_buff_to_skill_data[key] = {'name': self._BENEFIT_DATA[key]['szName'], 'times': []}
                        for times in buff_data:
                            self._other_benefit_buff_to_skill_data[key]['times'].append(times[:-1])
                    elif key in self._SELF_DATA:
                        # 添加进整合数据中
                        self._self_benefit_buff_to_skill_data[key] = {'name': self._SELF_DATA[key]['szName'], 'times': []}
                        for times in buff_data:
                            self._self_benefit_buff_to_skill_data[key]['times'].append(times[:-1])
                    else:
                        print(buff_id)
        pass





    def buff_effect(self):
        """
        统计某个增益所作用的技能\n
        :return:
        """
