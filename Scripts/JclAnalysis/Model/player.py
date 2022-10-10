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
        # self._dunfei_time = None
        # 盾飞buff持续时间

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

    @property
    def skill_events_by_id(self):
        return self._skill_event_by_id

    @property
    def dunfei_time_and_count(self):
        if 8391 not in self._buff:
            return 0
        else:
            _t = 0
            for item in self._buff[8391][1]:
                _t += item[1] - item[0]
            return _t, len(self._buff[8391][1])

    @property
    def buff_data(self):
        """
        出现过的所有buff
        :return:
        """
        return self._buff

    def update(self, data: Dict[int, Dict], player_id: int, npc_id: List, time_limit):
        """
        根据每行的数据内容以更新自身数据\n
        :param time_limit:
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
            # 添加时间限制
            if time_limit and item['msec'] > time_limit:
                break
            index: int
            item: Dict[str, Union[int, str, Dict]]
            self._type_update(item)
        # print(*[f"{i}: {j}\n" for i, j in self._skill.items()])
        # pass

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
                        if buff[1] in self._buff[buff_id]:
                            self._buff[buff_id][buff[1]].append((buff[0], msec, buff[1], buff[2], buff[3], buff[4]))
                        else:
                            self._buff[buff_id][buff[1]] = [(buff[0], msec, buff[1], buff[2], buff[3], buff[4])]
                    else:
                        self._buff[buff_id] = {buff[1]: [(buff[0], msec, buff[1], buff[2], buff[3], buff[4])]}
                self._waiting_buffs.clear()
            return

        # id必须为自身
        if not data['dwPlayerID'] == self.player_id:
            return
        if data['bDelete']:
            # 移除该buff的情况
            if new_buff_id not in self._waiting_buffs:
                # 在战斗记录外获取，战斗记录内消失的情况
                src_id = data['dwSkillSrcID']
                if src_id == 0:
                    src_id = data['dwPlayerID']
                if new_buff_id not in self._buff:
                    self._buff[new_buff_id] = {data['nLevel']: [(-1200, msec, data['nLevel'], data['nStackNum'], src_id, data['szName'])]}
                elif data['nLevel'] not in self._buff[new_buff_id]:
                    self._buff[new_buff_id][data['nLevel']] = [(-1200, msec, data['nLevel'], data['nStackNum'], src_id, data['szName'])]
                else:
                    self._buff[new_buff_id][data['nLevel']].append((-1200, msec, data['nLevel'], data['nStackNum'], src_id, data['szName']))
            # 绝刀怒气判定buff的保护
            elif new_buff_id == 9052:
                return
            else:
                if new_buff_id in {8271, 17772}:
                    # 寒甲特殊处理，按时长是否达到8000ms判断是否删除
                    if msec - self._waiting_buffs[new_buff_id][0] < 8000:
                        return
                old_buff = self._waiting_buffs.pop(new_buff_id)
                if new_buff_id in self._buff:
                    if old_buff[1] in self._buff[new_buff_id]:
                        self._buff[new_buff_id][old_buff[1]].append((old_buff[0], msec, old_buff[1], old_buff[2], old_buff[3], old_buff[4]))
                        # [level] = (add_time, del_time, nStackNum, dwSkillSrcID)
                    else:
                        self._buff[new_buff_id][old_buff[1]] = [(old_buff[0], msec, old_buff[1], old_buff[2], old_buff[3], old_buff[4])]
                else:
                    self._buff[new_buff_id] = {old_buff[1]: [(old_buff[0], msec, old_buff[1], old_buff[2], old_buff[3], old_buff[4])]}
        else:
            # 添加该buff的情况
            # 判断来源id
            src_id = data['dwSkillSrcID']
            if src_id == 0:
                src_id = data['dwPlayerID']
            # 特殊处理
            match new_buff_id:
                # 玉简特殊处理：盾飞时添加一次6层，后续要避免重复
                case 21648 if data['nStackNum'] == 6:
                    if 21648 in self._waiting_buffs:
                        buff_yj_ly = self._waiting_buffs[21648][2]
                        if buff_yj_ly == 6:
                            return

            if new_buff_id in self._waiting_buffs:
                # 判断等级
                if data['nLevel'] >= self._waiting_buffs[new_buff_id][1] or new_buff_id == 9052:
                    # 先取出该buff
                    old_buff = self._waiting_buffs.pop(new_buff_id)
                    if new_buff_id in self._buff:
                        if old_buff[1] in self._buff[new_buff_id]:
                            self._buff[new_buff_id][old_buff[1]].append(
                                (old_buff[0], msec, old_buff[1], old_buff[2], old_buff[3], old_buff[4]))
                            # [level] = (add_time, del_time, nStackNum, dwSkillSrcID)
                        else:
                            self._buff[new_buff_id][old_buff[1]] = [
                                (old_buff[0], msec, old_buff[1], old_buff[2], old_buff[3], old_buff[4])]
                    else:
                        self._buff[new_buff_id] = {
                            old_buff[1]: [(old_buff[0], msec, old_buff[1], old_buff[2], old_buff[3], old_buff[4])]}
                    # 添加新buff
                    # 绝刀怒气判定buff特殊处理
                    self._waiting_buffs[new_buff_id] = (msec, data['nLevel'], data['nStackNum'], src_id, data['szName'])
                else:
                    return
            else:
                # 直接添加
                self._waiting_buffs[new_buff_id] = (msec, data['nLevel'], data['nStackNum'], src_id, data['szName'])

    def _cast_skill(self, msec: int, data: Dict[str, Union[int, str, Dict]], *, status: Literal["dodge"] | None = None):
        """
        向时间-技能列表添加添加技能和技能释放时的buff\n
        :param msec:
        :param data: type_reader.read_type的返回值
        :return:
        """
        # 按技能统计用函数

        if status == 'dodge':
            data['bCriticalStrike'] = False
            data['tResultCount'] = {'dodge': 1}
            data['bReact'] = False

        if not data['dwCaster'] in self.id_list:
            # 非自身及自身的npc释放
            return
        if data['bReact']:
            # 吸血事件
            return

        dmg_sum = sum(data['tResultCount'].values())
        # 按技能分类
        # 用于查询某技能的所有释放时刻状态
        # 放在前面以防止部分技能的释放时刻事件被过滤掉
        skill_id = data['dwID']
        skill_level = data['dwLevel']
        if dmg_sum > 0:
            _type = 'damage'
        else:
            _type = 'cast'
        write_data = {
            "nType": _type,
            "bCritical": data['bCriticalStrike'],
            "tResult": data['tResultCount'],
            "tBuffs": {buff_id: (buff_data[1], buff_data[2], buff_data[3]) for buff_id, buff_data in
                       self._waiting_buffs.items()}
        }
        if skill_id in self._skill_event_by_id:
            if skill_level in self._skill_event_by_id[skill_id]:
                self._skill_event_by_id[skill_id][skill_level].update({msec: write_data})
            else:
                self._skill_event_by_id[skill_id][skill_level] = {"szName": data['szName'], msec: write_data}
        else:
            self._skill_event_by_id[skill_id] = {skill_level: {"szName": data['szName'], msec: write_data}}

        # 必须写在伤害统计前面，避免判定用子技能被过滤掉
        # 2022.9.25 盾飞后立即获得玉简效果
        match skill_id:
            case 13050:
                self._add_additional_buff(msec, 21648, '玉简·分山劲', 1, 6)

        if dmg_sum == 0 and not status == 'dodge':
            # 无伤害子技能
            return
        else:
            # 按目标再按时间分类
            # 用于进一步分析，得到表格内展示数据
            _target = data['dwTarget']
            if _target in self._skill_event_by_time_and_target:
                if msec in self._skill_event_by_time_and_target[_target]:
                    for i in range(50):
                        if i in self._skill_event_by_time_and_target[_target][msec]:
                            continue
                        else:
                            self._skill_event_by_time_and_target[_target][msec][i] = {
                                "szName": data['szName'],
                                "dwID": skill_id,
                                "dwLevel": skill_level,
                                "bCritical": data['bCriticalStrike'],
                                "tResult": data['tResultCount'],
                                "tBuffs": {buff_id: (buff_data[1], buff_data[2]) for buff_id, buff_data in self._waiting_buffs.items()}
                                #                   (level, layer)
                            }
                            break
                else:
                    self._skill_event_by_time_and_target[_target][msec] = {0: {
                        "szName": data['szName'],
                        "dwID": skill_id,
                        "dwLevel": skill_level,
                        "bCritical": data['bCriticalStrike'],
                        "tResult": data['tResultCount'],
                        "tBuffs": {buff_id: (buff_data[1], buff_data[2]) for buff_id, buff_data in
                                   self._waiting_buffs.items()}
                        #                   (level, layer)
                    }}
            else:
                self._skill_event_by_time_and_target[_target] = {msec: {0: {
                    "szName": data['szName'],
                    "dwID": skill_id,
                    "dwLevel": skill_level,
                    "bCritical": data['bCriticalStrike'],
                    "tResult": data['tResultCount'],
                    "tBuffs": {buff_id: (buff_data[1], buff_data[2]) for buff_id, buff_data in
                               self._waiting_buffs.items()}
                }}}




    def _add_additional_buff(self, msec: int, buff_id: int, buff_name: str, level: int, layer: int, src=0):
        """
        用于人工添加一些buff
        :param buff_id:
        :param buff_name:
        :param level:
        :param layer:
        :param persist:
        :param src:
        :return:
        """

        _buff_data = {
            'dwPlayerID': self.player_id,
            'bDelete': False,
            'nIndex': -1,
            'bCanCancel': 'buff',
            'dwBuffID': buff_id,
            'szName': buff_name,
            'nStackNum': layer,
            'nEndFrame': -1,
            'bInit': False,
            'nLevel': level,
            'dwSkillSrcID': src,
            'bIsValid': True
        }
        self._add_buff(msec, _buff_data)

