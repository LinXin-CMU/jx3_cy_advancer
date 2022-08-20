# coding: utf-8
# author: LinXin

from .ImitationPlayer.player import Player
from .CountSkill.skill_data_reshape import read_origin_skill_data
from CustomClasses.Exceptions import JclTypeError
from CustomClasses.TypeHints import FileReader


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

    @property
    def DATA_skill_to_table(self):
        """
        用于技能统计表的数据\n
        :return:
        """
        return self._skill_to_table


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




