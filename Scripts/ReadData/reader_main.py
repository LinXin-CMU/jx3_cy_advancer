from Scripts.ReadData.FileReader.file_reader import JclReader
from Scripts.ReadData.Equips.equip_reader import PlayerEquip
from Scripts.ReadData.Equips.attribute_calc import Attribute
from Scripts.Config.config import ConfigSetting
from CustomClasses.TypeHints import LuaTable
from CustomClasses.Exceptions import *

from lupa import LuaRuntime


class FileReader:
    """
    负责文件操作读取的各类流程
    """

    def __init__(self):
        self._data = None
        # 处理过的jcl文件原始数据
        self.config: ConfigSetting = ConfigSetting()
        # config对象
        self._player_id = None
        # 玩家id
        self._player_mount = None
        # 玩家心法
        self._npc_id = None
        # 玩家的npcid序列
        self._reader = JclReader()
        # 阅读jcl的类
        self._equip = PlayerEquip()
        # 读取并储存所有装备的类
        self.attributes = Attribute(self._equip)
        # 计算属性和输出各种格式属性的类
        self._lua = LuaRuntime()
        # 初始化lua解析器

    def run(self, current_player_name: str, filepath: str):
        # try:
        self._data = self._reader.run(filepath)
        # 读取原始数据
        self._get_player_info(current_player_name)
        # 查询到玩家id
        # 读取装备信息
        # except Exception as e:
        #     print(f"{e} at Scripts/ReadData/reader_main.py run")

    @property
    def player_id(self):
        return self._player_id

    @property
    def npc_id(self):
        if self._npc_id is None:
            self._npc_id = []
        return self._npc_id

    @property
    def id_to_name(self):
        return self._reader.record_info['name_data']

    @property
    def data(self):
        return self._data

    @property
    def csv_data(self):
        if self._data is not None:
            return self._reader.mark_to_csv_data()
        return None

    # 测试用
    @property
    def equip(self):
        """
        {
            key: position string,
            value: equip object
        }
        :return:
        """
        return {
            'HAT': self._equip['HAT'],
            'JACKET': self._equip['JACKET'],
            'BELT': self._equip['BELT'],
            'WRIST': self._equip['WRIST'],
            'BOTTOMS': self._equip['BOTTOMS'],
            'SHOES': self._equip['SHOES'],
            'NECKLACE': self._equip['NECKLACE'],
            'PENDANT': self._equip['PENDANT'],
            'RING_1': self._equip['RING_1'],
            'RING_2': self._equip['RING_2'],
            'PRIMARY_WEAPON': self._equip['PRIMARY_WEAPON'],
            'SECONDARY_WEAPON': self._equip['SECONDARY_WEAPON'],
        }

    @property
    def json_attribute(self) -> dict:
        return self.attributes.json_attributes

    @property
    def attribute(self) -> Attribute:
        return self.attributes

    def _get_player_info(self, player_name):
        """
        从记录中读取到当前玩家id和心法, 玩家的npcid\n
        :return:
        """
        try:
            # 先读取玩家id
            # 判断是否出现编码损坏
            _file_encode_error = False
            for player_id in self._reader.record_info['name_data']:
                _name = self._reader.record_info['name_data'][player_id]['szName']
                if "?" in _name:
                    _file_encode_error = True
                if _name == player_name:
                    # 记录玩家id
                    self._player_id = player_id
                    # 记录玩家心法
                    self._player_mount = self._reader.record_info['name_data'][player_id]['dwMountKungfuName']
                    # 直接添加心法到PlayerEquip.player_kungfu中
                    self.attributes.player_kungfu = self._player_mount
                    # 直接添加奇穴到PlayerEquip.player_talent中
                    self.attributes.player_talent = self._reader.record_info['name_data'][player_id]['aTalent']
                    break
            # 检测是否读取到玩家信息
            if self._player_id is None:
                if _file_encode_error:
                    raise JclFileEncodeError("jcl文件编码已损坏，请更换其他文件再复盘吧！")
                else:
                    raise NotFoundPlayerIDFromName("未能查询到玩家信息，请检查名称是否填写错误！")
            # 再读取npcid
            for npc_id in self._reader.record_info['name_data']:
                # 雇佣者为玩家
                _npc = self._reader.record_info['name_data'][npc_id]
                # 过滤掉玩家
                if 'dwEmployer' not in _npc:
                    continue
                if _npc['dwEmployer'] == self.player_id:
                    # 有显式名称且名称包含玩家
                    if player_name in _npc['szName']:
                        if self._npc_id is None:
                            self._npc_id = [npc_id]
                        else:
                            self._npc_id.append(npc_id)
        # 未检测到则抛出自定义异常
        except KeyError as e:
            print(f"KeyError {e} at Scripts/ReadData/reader_main.py _get_player_info: 未查询到对应玩家")
            raise NotFoundPlayerIDFromName("未能查询到玩家信息，请检查名称是否填写错误！")


    def get_equip_info(self):
        """
        调用：读取文件中的装备信息并储存
        :return:
        """
        origin_equip_info: LuaTable = self._reader.record_info['name_data'][self._player_id]['aEquip']
        # jcl中的原始数据
        # 读取装备属性
        self._equip.set_equip(origin_equip_info)
        # 20220729读取不到装备栏精炼镶嵌，暂不能使用

    def calc_attribute(self, write_in, current_index=None):
        """
        计算属性的上层入口, 用于控制计算时间
        :return:
        """
        if current_index == 3 or current_index is None:
            try:
                # 检测是否为装备栏设置页面切换至其他页面
                self.attributes.calc_attribute()
                self.config.add_config(section='equip', key='embedding_and_strength_default', value=write_in)
            except AttributeError as e:
                print(f"AttributeError: {e} at Scripts/ReadData/reader_main.py: 还未读取jcl装备数据或jcl不存在装备数据")

