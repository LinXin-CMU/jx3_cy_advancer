# coding: utf-8
# author: LinXin
# 负责检查存在的增益
# 初始化时就需要传入数据，自动分析后直接调用数据结论

from typing import Dict

from Scripts.JclAnalysis.CheckRecord.benefic_buffs import BENEFIT_BUFFS


class BeneficialChecker:

    def __init__(self):
        # self._BENEFIT_ID = [int(i.split('_')[0]) for i in BENEFIT_BUFFS.keys()]
        # 有效增益id
        self._other_benefit_buff_to_skill_data = {}
        self._self_benefit_buff_to_skill_data = {}

    def _filtrate_benefit_buff(self):
        """
        将数据按buff重新统计分类\n
        :return:
        """




    def _buff_effect(self):
        """
        统计某个增益所作用的技能\n
        :return:
        """
