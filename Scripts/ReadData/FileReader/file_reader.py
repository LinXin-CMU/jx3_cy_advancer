"""
用于读取jcl文件
input: x.jcl file
return: dict

"""
from lupa import LuaRuntime
from typing import Any, NoReturn
from datetime import timedelta

from Scripts.ReadData.FileReader.type_reader import TypeReader
from Sources.Jx3_Datas.Files.jcl_data import log_type, type_name, type_to_event_type
from CustomClasses.Exceptions import *


class JclReader:
    """
    jcl读取类

    """

    def __init__(self):
        self._data = None
        # 战斗记录整理后的数据
        self._csv_data = None
        # 需要导出为csv文件的数据
        self.record_info = None
        # 战斗记录中的特殊信息，如开始时间，玩家id等
        self._lua = LuaRuntime()
        self._type_reader = TypeReader()

    def run(self, filepath: str) -> dict | Any:
        # 新建一个dict用于储存jcl数据
        # dataframe太慢了
        # self.df = pd.DataFrame(columns=["frames", "timestamp", "msec", "event_type", "luadata"])
        self._data = {}
        self.record_info = {"name_data": {}}
        # 检查文件类型
        if not filepath.endswith('.jcl'):
            raise JclFileTypeError("this file is not a jcl file type")
        try:
            origin_file = open(filepath, 'r', encoding='gbk')
            # 读取原始文件
        except FileNotFoundError:
            print(f"file not found at {filepath}")
            raise NotFoundJclFileError
        else:
            # 开始逐行读取文件并进行分割
            reader = self._get_origin_data(origin_file)
            # reader.send(None)
            while True:
                try:
                    row, index = reader.send(None)
                    self._get_record_info(row)
                    self._data[index] = row
                except StopIteration:
                    break
            # 关闭文件
            origin_file.close()
            # 第二次遍历，标注信息
            self._mark_time()

        return self._data

    def _get_origin_data(self, origin_file: Any) -> Any:
        """
        将jcl文件分割并翻译\n
        :param origin_file:
        :return:
        """
        for index, line in enumerate(origin_file):
            # 分割每行
            line = line.strip().split()
            # 分析数据
            yield {"frame": int(line[1]), "timestamp": int(line[2]), "msec": int(line[3]),
                   "type": int(line[4]), "data": self._type_reader.read_type(line)}, index

            # 弹出当前行，等待下一步记录

    def _get_record_info(self, row: dict) -> NoReturn:
        """
        第一次遍历，将特殊数据记录到_record_info中\n
        :param row:
        :return:
        """
        # 特殊事件记录
        # 进入战斗时间，离开战斗时间
        match row['type']:
            case 1:
                if row['data']['bFighting']:
                    self.record_info['start_fight_time'] = {
                        'frame': row['frame'],
                        'timestamp': row['timestamp'],
                        'msec': row['msec']
                    }
                else:
                    self.record_info['end_fight_time'] = {
                        'frame': row['frame'],
                        'timestamp': row['timestamp'],
                        'msec': row['msec']
                    }
                    self.record_info['fight_time'] = row['data']['nDuring']

            # 玩家id， 玩家信息
            case 4 | 8:
                if row['type'] == 4:
                    if row['data']['dwID'] not in self.record_info['name_data']:
                        self.record_info['name_data'][row['data']['dwID']] = {
                            'szName': row['data']['szName'],
                            'dwForceName': row['data']['dwForceID'],
                            'dwMountKungfuName': row['data']['dwMountKungfuID'],
                            'nEquipScore': row['data']['nEquipScore'],
                            'aEquip': row['data']['aEquip'],
                            'aTalent': row['data']['aTalent']
                        }
                else:
                    # npc id
                    if row['data']['dwID'] not in self.record_info['name_data']:
                        self.record_info['name_data'][row['data']['dwID']] = {
                            'szName': row['data']['szName'],
                            'dwTemplateID': row['data']['dwTemplateID'],
                            'dwEmployer': row['data']['dwEmployer'],
                        }

    def _mark_time(self):
        """
        第二次遍历，标注时间，与下方的生成格式化记录隔离开\n
        :return:
        """
        for i in sorted(list(self._data.keys())):
            row = self._data[i]
            # 逻辑帧计算
            row['frame'] = row['frame'] - self.record_info['start_fight_time']['frame']
            # 时间戳计算
            row['timestamp'] = row['timestamp'] - self.record_info['start_fight_time']['timestamp']
            if row['timestamp'] >= 0:
                row['timestamp'] = timedelta(seconds=row['timestamp'])
            else:
                # 如果时间戳为负，手动添加负号
                row['timestamp'] = f"-{timedelta(seconds=abs(row['timestamp']))}"
            # 毫秒数计算
            row['msec'] = row['msec'] - self.record_info['start_fight_time']['msec']
            self._data[i] = row

    def mark_to_csv_data(self) -> NoReturn:
        """
        将特殊信息标记到数据中，以便于生成csv文件，如时间，角色名\n
        :param:
        :return:
        """
        # 清除数据
        self._csv_data = None
        # 对原始数据做有序遍历
        for i in sorted(list(self._data.keys())):
            row = self._data[i]
            if isinstance(row['type'], int):
                row['type'] = log_type[row['type']]
            # 过滤掉技能释放失败事件
            if row['type'] == 'SYS_MSG_UI_OME_SKILL_CAST_RESPOND_LOG':
                # del self._data[i]
                # continue
                pass
            # 翻译事件名称
            row['type_name'] = type_name[row['type']]
            if row['type_name'] == 13:
                row['data']['bDelete'] = "失去" if row['data']['bDelete'] else "获得",
                row['type_name'] = row['data'].pop('bDelete')[0] + 'BUFF'
            # 查找事件发生者
            row['event_name'] = None
            if 'szName' in row['data']:
                row['event_name'] = row['data'].pop('szName')
            elif 'bFight' in row['data']:
                row['event_name'] = row['data'].pop('bFight')
            # 查找事件大类
            row['event_type'] = type_to_event_type[row['type']]
            # 查找事件等级
            row['event_level'] = None
            _ = row['data']
            _level = None
            if 'nLevel' in _:
                _level = _.pop('nLevel')
            elif 'dwLevel' in _:
                _level = _.pop('dwLevel')
            row['event_level'] = _level
            # 查找事件层数
            row['event_layer'] = None
            _layer = None
            if 'nStackNum' in _:
                _layer = _.pop('nStackNum')
            row['event_layer'] = _layer
            # 查找释放者
            row['caster_name'] = None
            if 'dwCaster' in row['data']:
                row['caster_id'] = row['data']['dwCaster']
                try:
                    row['caster_name'] = self.record_info['name_data'][row['data']['dwCaster']]['szName']
                except KeyError:
                    row['caster_name'] = '未知目标'
                del row['data']['dwCaster']
            elif 'dwEmployer' in row['data']:
                row['caster_id'] = row['data']['dwEmployer']
                try:
                    row['caster_name'] = self.record_info['name_data'][row['data']['dwEmployer']]['szName']
                except KeyError:
                    row['caster_name'] = '未知目标'
                del row['data']['dwEmployer']
            # 查找目标
            row['target_name'] = None
            if 'dwTarget' in row['data']:
                row['target_id'] = row['data']['dwTarget']
                try:
                    row['target_name'] = self.record_info['name_data'][row['data']['dwTarget']]['szName']
                except KeyError:
                    row['target_name'] = '未知目标'
                del row['data']['dwTarget']
            elif row['type'] in ['PLAYER_FIGHT_HINT', 'NPC_ENTER_SCENE', 'NPC_LEAVE_SCENE']:
                try:
                    row['target_id'] = row['data']['dwID']
                    row['target_name'] = self.record_info['name_data'][row['data'].pop('dwID')]['szName']
                except KeyError:
                    row['target_name'] = '未知目标'
            elif row['type'] in ['SYS_MSG_UI_OME_COMMON_HEALTH_LOG', 'SYS_MSG_UI_OME_DEATH_NOTIFY']:
                try:
                    row['target_id'] = row['data']['dwCharacterID']
                    row['target_name'] = self.record_info['name_data'][row['data'].pop('dwCharacterID')]['szName']
                except KeyError:
                    row['target_name'] = '未知目标'
                try:
                    row['caster_id'] = row['data']['dwKiller']
                    row['caster_name'] = self.record_info['name_data'][row['data'].pop('dwKiller')]['szName']
                except KeyError:
                    row['caster_name'] = '未知目标'

            elif row['type'] == 'BUFF_UPDATE':
                try:
                    row['target_id'] = row['data']['dwPlayerID']
                    row['target_name'] = self.record_info['name_data'][row['data']['dwPlayerID']]['szName']
                except KeyError:
                    row['target_name'] = '未知目标'
                _ = row['data']['dwSkillSrcID']
                if not _ == 0:
                    try:
                        row['caster_id'] = _
                        row['caster_name'] = self.record_info['name_data'][_]['szName']
                    except KeyError:
                        row['caster_name'] = '未知目标'
                else:
                    row['caster_id'] = row['target_id']
                    row['caster_name'] = row['target_name']
                del row['data']['dwPlayerID'], row['data']['dwSkillSrcID']
            # 查找buff状态
            row['buff_type'] = None
            if row['type'] == 'BUFF_UPDATE':
                row['buff_type'] = row['data'].pop('bCanCancel')
            # 查找伤害
            row['effect_damage'] = None
            row['effect_health'] = None
            row['iscritical'] = None
            if row['type'] == 'SYS_MSG_UI_OME_SKILL_EFFECT_LOG':
                _ = row['data']['tResultCount']
                row['effect_damage'] = _['有效伤害']
                row['effect_health'] = _['有效治疗']
                row['iscritical'] = row['data'].pop('bCriticalStrike')
            # 查找事件id
            row['event_id'] = None
            _id = None
            _ = row['data']
            if 'szUUID' in _:
                _id = _.pop('szUUID')
            elif 'dwID' in _:
                _id = _.pop('dwID')
            elif 'dwBuffID' in _:
                _id = _.pop('dwBuffID')
            elif 'dwTalkerID' in _:
                _id = _.pop('dwTalkerID')
            elif 'dwMemberID' in _:
                _id = _.pop('dwMemberID')
            elif 'dwSkillID' in _:
                _id = _.pop('dwSkillID')
            elif 'dwCharacterID' in _:
                _id = _.pop('dwCharacterID')
            if _id is not None:
                row['event_id'] = _id
            # 结束帧计算
            if 'nEndFrame' in row['data']:
                row['data']['nEndFrame'] -= self.record_info['start_fight_time']['frame']
            # 删除部分值
            for key in ['bReact', 'nCount', 'nIndex', 'bInit', 'bIsValid']:
                if key in row['data']:
                    del row['data'][key]

            # 赋值回原数据
            if self ._csv_data is None:
                self._csv_data = {0: row}
            else:
                self._csv_data[i] = row

        return self._csv_data
