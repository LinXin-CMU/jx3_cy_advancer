# coding: utf-8
# author: LinXin
# 从skill_event_by_id中提取技能轴和增益数据, 并将技能轴数据提交给评分模块

from typing import Dict

from .CheckRecord.major_skill_check import MajorSkillChecker
from .CheckRecord.benefit_buff_check import BeneficialChecker
from CustomClasses.TypeHints import FileReader, Player



class MainChecker:

    def __init__(self, data_address: Player, file_address: FileReader):
        self._major_checker = MajorSkillChecker()
        self._benefit_checker = BeneficialChecker()
        # 复盘子类
        self._reader = file_address
        self._player = data_address
        self._attribute = self._reader.attribute
        # 玩家数据

    def run(self):
        """
        执行技能和增益复盘\n
        :return:
        """
        # 获取生成器对象
        major_gen = self._major_checker.get_work_gen(kungfu=self._attribute.player_kungfu)

        # for loop
        try:
            for skill_id, _ in self._player.skill_events_by_id.items():
                for skill_level, skill_data in _.items():
                    skill_name = skill_data.pop('szName')
                    for msec, cast_state in skill_data.items():
                        result = cast_state['tResult']
                        buff = cast_state['tBuffs']
                        # 发送内容
                        major_gen.send((msec, skill_id, skill_level, skill_name, buff))
        # try:
        finally:
            major_gen.close()
            print(*[f"{i}: {self._major_checker.major_skill_list[i]}\n" for i in sorted(self._major_checker.major_skill_list.keys())])
            print(self._major_checker.major_skill_analysis)
        # except StopIteration:
        #     pass







