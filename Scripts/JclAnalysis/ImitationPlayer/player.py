# coding: utf-8
# author: LinXin
from lupa import LuaRuntime
from typing import Dict, Union, Literal, List


class Player:
    """
    模拟玩家，储存每一时刻自身状态
    """

    def __init__(self):
        self.player_id = None
        # 玩家id
        self.npc_id = None
        # 玩家的npcid
        self.id_list = None
        # id集合
        self.lua = LuaRuntime()
        self._buff = None
        # {buff_id: {start1: (end1, level, layer)}}
        self._skill_event_by_id = None
        # 技能按id分类
        # {time: {id, level, critical, result, buffs}}
        self._skill_event_by_time_and_target = None
        # 技能按时间分类
        self._skill_event_by_target = None
        # 技能按目标分类
        self._waiting_buffs = None
        # {buff_id: (start, level, layer)}
        # 未被结束的buff

    # def __str__(self):
    #     pass

    # def check_buff(self, msec: int) -> Dict[int, tuple[str, int]]:
    #     """
    #     检查某一时间点的buff情况\n
    #     :param msec:
    #     :return:
    #     """
    #     for start_time, buff_data in self._buff.items():
    #         if
    #     已通过 self._skill 结构代替

    @property
    def skill_events_by_time(self):
        return self._skill_event_by_time_and_target



    def update(self, data: Dict[int, Dict], player_id: int, npc_id: List):
        """
        根据每行的数据内容以更新自身数据\n
        :param npc_id:
        :param data:
        :param player_id:
        :return:
        """
        self.player_id = player_id
        self.npc_id = npc_id
        self.id_list = [i for i in self.npc_id]
        self.id_list.append(self.player_id)
        self._buff = {}
        self._waiting_buffs = {}
        self._skill_event_by_id = {}
        self._skill_event_by_time_and_target = {}

        for index, item in data.items():
            index: int
            item: Dict[str, Union[int, str, Dict]]
            self._type_update(item)
        # print(*[f"{i}: {j}\n" for i, j in self._skill.items()])

    def _type_update(self, item: Dict[str, Union[int, str, Dict]]):
        """
        根据类型查找到对应记录\n
        :param data:
        :return:
        """
        data_type: str = item['type']
        data_value: Dict[str, Union[int, str]] = item['data']
        match data_type:
            # buff获得/消失，更新buff状态
            # 技能释放时间点
            case 1:
                # 终止事件
                if not data_value['bFighting']:
                    self._add_buff(item['msec'], status='end')
            case 13:
                self._add_buff(item['msec'], data_value)
            case 21:
                self._cast_skill(item['msec'], data_value)
            case 26:
                # 技能被闪避事件
                self._cast_skill(item['msec'], data_value, status='dodge')

        # print(self._waiting_buffs)

    def _add_buff(self, msec: int, data: Dict[str, Union[int, str, Dict]] = None, *, status: Literal["end"] | None = None):
        """
        读取状态栏中待结束buff，添加已完结buff栏，向状态栏添加未完结buff\n
        :param msec:
        :param data:
        :return:
        """
        # {'dwPlayerID', 'bDelete', 'nIndex', 'bCanCancel', 'dwBuffID', 'szName', 'nStackNum', 'nEndFrame', 'bInit', 'nLevel',
        #  'dwSkillSrcID', 'bIsValid', }
        # 1. 如果缓冲区不存在该buff
        #     1.1 如果类型为添加buff
        #           在缓冲区添加该buff
        #     1.2 如果类型为移除buff
        #           返回
        # 2. 如果缓冲区存在该buff
        #     2.1 如果类型为添加buff
        #           在缓冲区中移除该buff
        #           将该buff添加至缓冲区
        #     2.2 如果类型为移除buff
        #           读取该buff添加时间
        #           记录该buff数据
        #           在缓冲区中移除该buff
        if data is not None:
            new_buff_id = data['dwBuffID']
        else:
            new_buff_id = -1


        if status == 'end':
            # 结束时的情况
            if len(self._waiting_buffs) > 0:
                for buff_id, buff in self._waiting_buffs.items():
                    # 将所有等待buff添加至玩家状态
                    if buff_id in self._buff:
                        self._buff[buff_id][buff[0]] = (msec, buff[1], buff[2])
                    else:
                        self._buff[buff_id] = {buff[0]: (msec, buff[1], buff[2])}
                self._waiting_buffs.clear()
            return

        # id必须为自身
        if not data['dwPlayerID'] == self.player_id:
            return
        if data['bDelete']:
            # 移除该buff的情况
            if new_buff_id not in self._waiting_buffs:
                return
            else:
                old_buff = self._waiting_buffs.pop(new_buff_id)
                if new_buff_id in self._buff:
                    self._buff[new_buff_id][old_buff[0]] = (msec, old_buff[1], old_buff[2])
                else:
                    self._buff[new_buff_id] = {old_buff[0]: (msec, old_buff[1], old_buff[2])}
        else:
            # 添加该buff的情况
            if new_buff_id in self._waiting_buffs:
                # 判断等级
                if data['nLevel'] >= self._waiting_buffs[new_buff_id][1]:
                    # 添加新buff
                    self._waiting_buffs[new_buff_id] = (msec, data['nLevel'], data['nStackNum'])
                else:
                    return
            else:
                # 直接添加
                self._waiting_buffs[new_buff_id] = (msec, data['nLevel'], data['nStackNum'])

    def _cast_skill(self, msec: int, data: Dict[str, Union[int, str, Dict]], *, status: Literal["dodge"] | None = None):
        """
        向时间-技能列表添加添加技能和技能释放时的buff\n
        :param msec:
        :param data: type_reader.read_type的返回值
        :return:
        """
        # 按技能统计用函数
        def _check_buffs(tBuffs: Dict):
            """
            用于更新buff的内部函数
            :param tBuffs:
            :return:
            """
            for buff_id, buff_value in write_data['tBuffs'].items():
                # buff_value: tuple('nLevel', 'nStackNum')
                if buff_id in tBuffs:
                    if buff_value[0] in tBuffs[buff_id]:
                        _t = tBuffs[buff_id][buff_value[0]]
                        _t['nCount'] += 1
                        _t['nLayer'] += buff_value[1]
                        # tBuffs[buff_id][buff_value[0]] = _t
                    else:
                        tBuffs[buff_id][buff_value[0]] = {
                            'nCount': 1,
                            'nLayer': buff_value[1]
                        }
                else:
                    tBuffs[buff_id] = {
                        buff_value[0]: {
                            'nCount': 1,
                            'nLayer': buff_value[1]
                        }
                    }
            return tBuffs

        if status == 'dodge':
            data['bCriticalStrike'] = False
            data['tResultCount'] = {'dodge': 1}
            data['bReact'] = False

        if not data['dwCaster'] in self.id_list:
            # 自身及自身的npc释放
            return
        if data['bReact']:
            # 吸血事件
            return
        dmg_sum = sum(data['tResultCount'].values())
        if dmg_sum == 0 and not status == 'dodge':
            # 无伤害子技能
            return
        else:
            skill_id = data['dwID']
            skill_level = data['dwLevel']
            # 按目标再按时间分类
            # 用于进一步分析，得到表格内展示数据
            _target = data['dwTarget']
            if _target in self._skill_event_by_time_and_target:
                self._skill_event_by_time_and_target[_target][msec] = {
                    "szName": data['szName'],
                    "dwID": skill_id,
                    "dwLevel": skill_level,
                    "bCritical": data['bCriticalStrike'],
                    "tResult": data['tResultCount'],
                    "tBuffs": {buff_id: (buff_data[1], buff_data[2]) for buff_id, buff_data in self._waiting_buffs.items()}
                }
            else:
                self._skill_event_by_time_and_target[_target] = {msec: {
                    "szName": data['szName'],
                    "dwID": skill_id,
                    "dwLevel": skill_level,
                    "bCritical": data['bCriticalStrike'],
                    "tResult": data['tResultCount'],
                    "tBuffs": {buff_id: (buff_data[1], buff_data[2]) for buff_id, buff_data in
                               self._waiting_buffs.items()}
                }}
            # 按技能分类
            # 用于查询某技能的所有释放时刻状态
            write_data = {
                "bCritical": data['bCriticalStrike'],
                "tResult": data['tResultCount'],
                "tBuffs": {buff_id: (buff_data[1], buff_data[2]) for buff_id, buff_data in self._waiting_buffs.items()}
            }
            if skill_id in self._skill_event_by_id:
                if skill_level in self._skill_event_by_id[skill_id]:
                    self._skill_event_by_id[skill_id][skill_level].update({msec: write_data})
                else:
                    self._skill_event_by_id[skill_id][skill_level] = {msec: write_data}
            else:
                self._skill_event_by_id[skill_id] = {skill_level: {msec: write_data}}







