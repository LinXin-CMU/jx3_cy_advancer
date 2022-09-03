# coding: utf-8
# author: LinXin

from .ImitationPlayer.player import Player
from .CheckRecord.skill_data_reshape import read_origin_skill_data
from Scripts.JclAnalysis.checker_main import MainChecker
from CustomClasses.Exceptions import JclTypeError
from CustomClasses.TypeHints import FileReader, Attribute


class Analysis:
    """
    读取文件，整理数据，计算中间值，计算评分，输出详细信息
    """
    def __init__(self, data_address: FileReader):
        self._reader = data_address
        # 先储存FileReader object，以备调用data
        self.data = None
        # jcl基础数据
        self._player = Player()
        # 玩家对象，储存状态
        self._skill_to_table = None
        # 用于技能统计表的数据
        self.attribute: Attribute = data_address.attribute
        # Attribute类
        self._data_checker = MainChecker(self._player, self._reader)

    @property
    def DATA_skill_to_table(self):
        """
        用于技能统计表的数据\n
        :return:
        """
        return self._skill_to_table

    @property
    def skill_analysis_data(self):
        """
        用于循环页上半部分的数据\n
        :return: Dict{'major_skill_list', 'analysis', 'operate_list'}
        """
        return {
            "major_skill_list": self._data_checker.current_kungfu_skills,
            "analysis": self._data_checker.major_skill_analysis,
            "operate_list": self._data_checker.operate_skill_list
        }

    # @property
    def get_operate_data(self):
        """
        用于循环页下半部分的数据\n
        :return:
        """
        return self._get_all_operate_data()



    def run(self):
        self.data = self._reader.data
        # 动态获取一次当前data并更新到自身属性
        player_id = self._reader.player_id
        npc_id = self._reader.npc_id
        # data类型校验
        if not (isinstance(self.data, dict) and isinstance(self.data[1], dict)):
            raise JclTypeError
        self._player.update(self.data, player_id, npc_id)
        # 这里是得到按不同目的分类的buff和技能数据
        # 开始对技能统计数据的处理
        # 1. 整理技能至可供表格展示的状态
        self._skill_to_table = read_origin_skill_data(self._player.skill_events_by_time, self._reader.id_to_name)
        # print(*[f"{i}: {j}\n" for i, j in data.items()])
        # 2. 读取技能轴和增益
        self._data_checker.run()


    def _get_all_operate_data(self):
        """
        提供复盘图片所需的数据
        :return:
        """
        # 战斗时间
        fight_time = self._reader.record_info['fight_time']
        # 技能数据
        skill_data = self._data_checker.all_skill_analysis

        return [fight_time, skill_data]




