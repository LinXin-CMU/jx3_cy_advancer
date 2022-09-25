# coding: utf-8
# author: LinXin

from .Model.player import Player
from .Model.npc import Npc
from .CheckRecord.skill_data_reshape import read_origin_skill_data
from .Mark.operate_marker import OperateMarker
from .checker_main import MainChecker
from CustomClasses.Exceptions import JclTypeError
from CustomClasses.TypeHints import FileReader, Attribute

from concurrent.futures import ThreadPoolExecutor, wait


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
        self._npc = Npc()
        # boss对象，储存状态
        self._skill_to_table = None
        # 用于技能统计表的数据
        self.attribute: Attribute = data_address.attribute
        # Attribute类
        self._data_checker = MainChecker(self._player, self._reader)
        # 操作类
        self._operate_checker = OperateMarker()
        # 玩家战斗数据的整理后记录
        self._skill_analysis_data = None

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
        self._skill_analysis_data = {
            "major_skill_list": self._data_checker.current_kungfu_skills,
            "analysis": self._data_checker.major_skill_analysis,
            "operate_list": self._data_checker.operate_skill_list
        }
        return self._skill_analysis_data

    # @property
    def get_operate_data(self):
        """
        用于循环页下半部分的数据\n
        :return:
        """
        return *self._get_all_operate_data(), self._data_checker.benefit_buffs, self._npc.target_buff_data


    def run(self, time_limit=0):
        pool = ThreadPoolExecutor(3)

        self.data = self._reader.data
        # 动态获取一次当前data并更新到自身属性
        player_id = self._reader.player_id
        npc_id = self._reader.npc_id
        # data类型校验
        if not (isinstance(self.data, dict) and isinstance(self.data[1], dict)):
            raise JclTypeError

        # future1 = pool.submit(self._player.update, self.data, player_id, npc_id)
        # # 这里是得到按不同目的分类的buff和技能数据
        # future2 = pool.submit(self._npc.run, self.data, self._reader.boss_name, player_id, self._reader.record_info)
        # wait([future1, future2], return_when='ALL_COMPLETED')
        # print(self._npc.target_buff_data)

        # # 开始对技能统计数据的处理
        # # 1. 整理技能至可供表格展示的状态
        # future3 = pool.submit(read_origin_skill_data, self._player.skill_events_by_time, self._reader.id_to_name)
        # # 2. 读取技能轴和增益
        # future4 = pool.submit(self._data_checker.run)
        # # 3. 读取buff序列并分析
        # future5 = pool.submit(self._data_checker.run_buff)
        #
        # wait([future3, future4, future5], return_when='ALL_COMPLETED')
        # self._skill_to_table = future3.result()

        self._player.update(self.data, player_id, npc_id, time_limit)
        # 这里是得到按不同目的分类的buff和技能数据
        self._npc.run(self.data, self._reader.boss_name, player_id, self._reader.record_info, time_limit)

        # 开始对技能统计数据的处理
        # 1. 整理技能至可供表格展示的状态
        self._skill_to_table = read_origin_skill_data(self._player.skill_events_by_time, self._reader.id_to_name)
        # 2. 读取技能轴和增益
        self._data_checker.run()
        # 3. 读取buff序列并分析
        self._data_checker.run_buff()


    def run_marker(self, time_limit=0):
        # 开始进入评分模块
        if time_limit:
            _fight_time = int(time_limit / 1000)
        else:
            _fight_time = self._reader.record_info['end_fight_time']['timestamp'] - \
                          self._reader.record_info['start_fight_time']['timestamp']
        # 1. 读取玩家数据
        self._operate_checker.basic_setting(self.attribute, _fight_time)
        # 2. 计算评分
        if self._skill_analysis_data is None:
            return
        ret = self._operate_checker.run(self._skill_analysis_data)
        return ret

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




