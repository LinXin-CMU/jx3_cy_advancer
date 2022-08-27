# coding: utf-8
# author: LinXin
# 负责检查存在的增益
# 初始化时就需要传入数据，自动分析后直接调用数据结论

from typing import Dict

from Scripts.JclAnalysis.CheckRecord.benefic_buffs import BENEFIT_BUFFS


class BeneficialChecker:

    def __init__(self, skill_event_by_id: Dict):
        self._skills_origin_data = skill_event_by_id
        # 按技能id分类的技能数据，包含每个技能的释放时间和释放时buff
        self._BENEFIT_ID = [int(i.split('_')[0]) for i in BENEFIT_BUFFS.keys()]
        # 有效增益id
        self._other_benefit_buff_to_skill_data = {}
        self._self_benefit_buff_to_skill_data = {}

    def _filtrate_benefit_buff(self):
        """
        将数据按buff重新统计分类\n
        :return:
        """
        for skill_id, skill_data in self._skills_origin_data.items():
            for skill_level, level_data in skill_data.items():
                for msec, buff_data in level_data.items():
                    # 过滤治疗技能和无伤害技能
                    if '有效伤害' not in buff_data['tResult'] or buff_data['tResult']['有效伤害'] == 0:
                        continue
                    # 过滤非增益技能



    def _buff_effect(self):
        """
        统计某个增益所作用的技能\n
        :return:
        """
