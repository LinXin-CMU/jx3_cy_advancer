# coding: utf-8
# author: LinXin
# 通过检测玩家对目标释放的技能判断目标身上是否有某些buff及buff的持续时间
from typing import Dict, Union, Literal
from collections import namedtuple



import_kungfu = {'傲血战意', '铁牢律', '离经易道', '太虚剑意', '冰心诀', '云裳心经', '焚影圣诀', '明尊琉璃体', '分山劲', '铁骨衣', '莫问', '相知'}
# 技能id: [buffid]
import_skill = {403: [661, 12717], 180: [23305], 21317: [16680], 23208: [16330], 23216: [16331], 23218: [16330],
                23211: [16330], 23210: [16365], 22609: [15850], 13050: [8248], 13054: [], 8249: [8249], 15511: [10530, 10533],
                23240: [10530, 10533], 23234: [], 23235: [], 23236: [], 23826: [], 23835: [], 23836: [], 3980: [4058],
                3963: [4418], 29187: [8249], 29188: [8249], 29186: [8249], 29185: [8249], 13308: [8249], 20989: [8249]}


buff = namedtuple('buff', ['id', 'level', 'layer', 'persist_msec', 'src_name'])
buff_time = namedtuple('inside_buff', ['start', 'end', 'layer', 'src_name'])
buff_res = namedtuple('only_for_target_buff_result', ['start', 'end', 'level', 'layer', 'src_name'])

def delete_self(func):
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret is not None:
            del func
        return ret
    return inner


class Npc:

    def __init__(self):
        self._blood_data = {}
        self._record_info = None
        self.npc_name = None
        self.player_id = None
        self._buffs = {}
        # {npc_id: {buff_id: {level: [(start_time, end_time)]}}}}
        # 记录所有可能释放目标易伤的玩家id
        # id: kungfu
        self._checked_players = {}
        # 记录释放过特效武器的玩家和时间
        self._special_weapon_caster = {}
        # 返回用数据
        self._targets_buff_data = {}


    def _get_target_player(self):
        """
        筛选能释放所需buff的技能的玩家\n
        :return:
        """
        self._checked_players = {}
        player_infos = self._record_info['name_data']
        for player_id, player_data in player_infos.items():
            if 'dwMountKungfuName' in player_data:
                if player_data['dwMountKungfuName'] in import_kungfu:
                    self._checked_players[player_id] = player_data['dwMountKungfuName']


    def run(self, data: Dict[int, Dict[str, Union[str, int, Dict[str, Union[int, str, bool]]]]], npc_name: str, player_id: int, record_info: Dict, time_limit: int):
        """
        外层接口
        :return:
        """
        self._record_info = record_info
        self.npc_name = npc_name
        self.player_id = player_id
        self._buffs = {}
        self._special_weapon_caster = {}
        self._get_target_player()

        for index, _data in data.items():
            # 添加时间限制
            if time_limit and _data['msec'] > time_limit:
                break
            if _data['type'] == 21:
                _caster = _data['data']['dwCaster']
                _target = _data['data']['dwTarget']
                if _target in self._record_info['name_data']:
                    _target_name = self._record_info['name_data'][_target]['szName']
                else:
                    continue
                if _caster in self._checked_players and _target_name == self.npc_name:
                    if _data['data']['dwID'] in import_skill:
                        if '吸血' in _data['data']['tResultCount']:
                            continue
                        _msec = _data['msec']
                        _skill_id = _data['data']['dwID']
                        _skill_level = _data['data']['dwLevel']
                        self._be_casted(_msec, _caster, _target, _skill_id, _skill_level)
        # print(self._buffs)
        self._get_target_buff_data()

        pass

    def _be_casted(self, msec, caster, target, skill_id, skill_level):
        """
        用于筛选当前技能是否是会添加所需buff的技能，如是的话会调用添加buff\n
        :return:
        """
        _add_buff = None
        kungfu = self._checked_players.get(caster)
        caster_data = self._record_info['name_data'].get(caster)
        caster_name = caster_data.get('szName')



        match kungfu:

            case '傲血战意' | '铁牢律':
                if skill_id == 403:
                    if kungfu == '傲血战意' or '劲风' not in caster_data['aTalent']:
                        self._add_buff(msec, caster_name, target, buff(661, 30, 1, 14*1000, caster_name))
                    else:
                        self._add_buff(msec, caster_name, target, buff(12717, 30, 1, 14 * 1000, caster_name))

            case '焚影圣诀' | '明尊琉璃体' | '离经易道':
                if skill_id == 3963:
                    self._add_buff(msec, caster_name, target, buff(4418, 1, 1, 12*1000, caster_name))
                elif skill_id in {3980, 180}:
                    if 'MingHua' not in self._special_weapon_caster:
                        self._special_weapon_caster['MingHua'] = self._logic_AllDmgCoef()
                    check = self._special_weapon_caster['MingHua']
                    if skill_id == 3980:
                        buff_jh = buff(4058, 1, 1, 15*1000, caster_name)
                        if check(msec, buff_jh):
                            self._add_buff(msec, caster_name, target, buff_jh)
                    elif skill_id == 180:
                        buff_qs = buff(23305, 1, 1, 18*1000, caster_name)
                        if check(msec, buff_qs):
                            self._add_buff(msec, caster_name, target, buff_qs)

            case '太虚剑意':
                if skill_id == 21317:
                    # 画影残月
                    buff_hy = buff(16680, 1, 1, 15*1000, caster_name)
                    self._add_buff(msec, caster_name, target, buff_hy)

            case '分山劲' | '铁骨衣':
                if skill_id == 13050:
                    buff_xr = buff(8248, 1, 1, 25*1000, caster_name)
                    self._add_buff(msec, caster_name, target, buff_xr)
                elif skill_id == 13054:
                    buff_xr = self._get_buff(msec, caster_name, target, 8248, 1)
                    if buff_xr is not None:
                        self._add_buff(buff_xr.start, caster_name, target, buff(8248, 1, 1, msec-buff_xr.start, caster_name))
                elif skill_id in {29187, 29188, 29186, 29185, 13308, 20989, 8249}:
                    # 流血部分
                    if not caster == self.player_id:
                        return

                    if target in self._blood_data:
                        self._blood_data[target].append((msec, skill_id))
                    else:
                        self._blood_data[target] = [(msec, skill_id)]
                    # blood_data.append((msec, skill_id))
                    pass

            case '莫问' | '相知':
                if kungfu == '莫问':
                    imports = {23234, 23235, 23236, 15511, 23240}
                else:
                    imports = {23826, 23835, 23836, 15511, 23240}
                if skill_id not in imports:
                    return
                if caster not in self._special_weapon_caster:
                    # 第一次使用风雷
                    _last_use = self._logic_ChangGe(caster_name)
                    _last_use['func'](msec, skill_id)
                    self._special_weapon_caster[caster] = [_last_use]
                else:
                    _last_use = self._special_weapon_caster[caster][-1]
                    if msec - _last_use['time'] < _last_use['persist']:
                        # 同一次风雷
                        ret = _last_use['func'](msec, skill_id)
                        if ret is not None:
                            self._add_buff(msec, caster_name, target, ret)
                    else:
                        # 第二次使用风雷
                        _last_use = self._logic_ChangGe(caster_name)
                        _last_use['func'](msec, skill_id)
                        self._special_weapon_caster[caster].append(_last_use)


    def _add_buff(self, start_time: int, caster_name, target: int, _buff: buff):
        """
        添加所需buff\n
        :return:
        """
        end_time = start_time + _buff.persist_msec
        # 开始填入
        if caster_name not in self._buffs:
            self._buffs[caster_name] = {
                target: {
                    _buff.id: {
                        _buff.level: [buff_time(start_time, end_time, _buff.layer, _buff.src_name)]
                    }
                }
            }
        elif target not in self._buffs[caster_name]:
            self._buffs[caster_name][target] = {
                _buff.id: {
                    _buff.level: [buff_time(start_time, end_time, _buff.layer, _buff.src_name)]
                }
            }
        else:
            if _buff.id not in self._buffs[caster_name][target]:
                self._buffs[caster_name][target][_buff.id] = {
                    _buff.level: [buff_time(start_time, end_time, _buff.layer, _buff.src_name)]
                }
            else:
                if _buff.level not in self._buffs[caster_name][target][_buff.id]:
                    self._buffs[caster_name][target][_buff.id][_buff.level] = [buff_time(start_time, end_time, _buff.layer, _buff.src_name)]
                else:
                    self._buffs[caster_name][target][_buff.id][_buff.level].append(buff_time(start_time, end_time, _buff.layer, _buff.src_name))

    def _get_buff(self, msec, caster_name, target, buff_id, buff_level, *, del_buff=True) -> buff_time:
        """
        读取所需buff\n
        :return:
        """
        ret = None
        if caster_name in self._buffs:
            if target in self._buffs[caster_name]:
                if buff_id in self._buffs[caster_name][target]:
                    if buff_level in self._buffs[caster_name][target][buff_id]:
                        if del_buff:
                            ret = self._buffs[caster_name][target][buff_id][buff_level].pop(-1)
                            if ret.end < msec:
                                self._buffs[caster_name][target][buff_id][buff_level].append(ret)
                                ret = None
                        else:
                            ret = self._buffs[caster_name][target][buff_id][buff_level][-1]

        return ret

    def _get_target_buff_data(self):
        """
        将buff数据整理成返回的格式\n
        :return:
        """
        self._targets_buff_data = {}
        _target_count = {}

        # 添加npc的流血buff
        self._logic_LiuXue()

        for src_name, targets_data in self._buffs.items():
            for target, buffs_data in targets_data.items():
                if target not in self._targets_buff_data:
                    self._targets_buff_data[target] = {}
                    _target_count[target] = 0

                for buff_id, buff_data in buffs_data.items():
                    for buff_level, buff_times in buff_data.items():
                        key = f"{buff_id}_{buff_level}"
                        if key not in self._targets_buff_data[target]:
                            self._targets_buff_data[target][key] = {
                                'name': buff_id,
                                'times': [(i.start, i.end, buff_level, i.layer, src_name) for i in buff_times]
                            }
                            _target_count[target] += len(buff_times)
                        else:
                            self._targets_buff_data[target][key]['times'] += \
                                [(i.start, i.end, buff_level, i.layer, src_name) for i in buff_times]
                            _target_count[target] += len(buff_times)
        # 添加计数
        for target_id, target_buff in self._targets_buff_data.items():
            self._targets_buff_data[target_id]['name'] = self.npc_name
            self._targets_buff_data[target_id]['count'] = _target_count[target_id]
            # 减去重叠的小破风
            if '661_30' in target_buff and '12717_30' in target_buff:
                self._logic_PoFeng(target_id, target_buff)



    @property
    def target_buff_data(self):
        return self._targets_buff_data

    # 下方的逻辑用于多技能关联

    @staticmethod
    def _logic_ChangGe(src_name):
        """
        针对风雷瑶琴剑的特殊判定\n
        :return:
        """
        casted = ''


        nickname = {
            23234: '1',
            23826: '1',
            23235: '2',
            23835: '2',
            23236: '3',
            23836: '3',
        }

        res_buffs = {
            '131': buff(10533, 1, 1, 20*1000, src_name),
            '311': buff(10533, 1, 1, 20*1000, src_name),
            '113': buff(10533, 6, 1, 20*1000, src_name),
            '333': buff(10530, 6, 1, 20*1000, src_name)
        }

        start_time = -1

        persist = 60 * 1000

        @delete_self
        def cast(msec, skill_id):
            """
            判断风雷瑶琴剑的实际逻辑\n
            :return:
            """
            nonlocal casted, start_time
            if skill_id in nickname:
                casted += nickname[skill_id]
            if skill_id in {15511, 23240}:
                # 根据技能序列判断返回buff
                if casted in res_buffs:
                    return res_buffs[casted]
            elif casted == '':
                start_time = msec

        inner = {
            'func': cast,
            'time': start_time,
            'persist': persist
        }

        return inner

    @staticmethod
    def _logic_AllDmgCoef():
        latest_buff: buff | None = None
        latest_time: int = 0

        def inner(msec, _buff: buff):
            nonlocal latest_buff, latest_time
            if latest_buff is None:
                latest_buff = _buff
                latest_time = msec
                return True
            else:
                if _buff.id == 23305:
                    # 秋肃
                    latest_buff = _buff
                    latest_time = msec
                    return True
                else:
                    if latest_buff.persist_msec + latest_time < msec:
                        # 上一个buff已经消失, 可以添加
                        latest_buff = _buff
                        latest_time = msec
                        return True
                    else:
                        return False
        return inner

    def _logic_PoFeng(self, target_id, target_buff):
        # 先遍历劲风破风, 获取劲风破风时间轴
        jf_times = []
        for jf_time in target_buff['12717_30']['times']:
            if len(jf_times) == 0:
                jf_times.append((jf_time[0], jf_time[1]))
            else:
                past_time = jf_times[-1]
                if jf_time[0] < past_time[1]:
                    jf_times[-1] = (past_time[0], max(past_time[1], jf_time[1]))
                else:
                    jf_times.append((jf_time[0], jf_time[1]))
        # 对于每一个小破风，检测其是否被包含在劲风破风里
        # 双指针
        p_pf = 0  # 661-破风
        p_jf = 0  # 12717-劲风
        buff_p_pf = target_buff['661_30']['times']
        buff_p_jf = jf_times
        while True:
            # 更新下标界限
            stop_pf = len(buff_p_pf) - 1
            stop_jf = len(buff_p_jf) - 1
            # 读取buff
            buff_pf: buff_res = buff_res(*buff_p_pf[p_pf])
            buff_jf: buff_res = buff_res(*buff_p_jf[p_jf], 1, 1, buff_pf.src_name)
            # 布尔运算
            if buff_pf.start >= buff_jf.start and buff_pf.end <= buff_jf.end:
                # 破风完全在劲风内，移除破风
                del self._targets_buff_data[target_id]['661_30']['times'][p_pf]
            elif buff_pf.start < buff_jf.start and buff_pf.end > buff_jf.end:
                # 劲风完全在破风内，拆分破风
                head = (buff_pf.start, buff_jf.start - 1, buff_pf.level, buff_pf.layer, buff_pf.src_name)
                tail = (buff_jf.end + 1, buff_pf.end, buff_pf.level, buff_pf.layer, buff_pf.src_name)
                self._targets_buff_data[target_id]['661_30']['times'] = buff_p_pf[:p_pf] + [head, tail] + buff_p_pf[
                                                                                                          p_pf + 1:]
            elif buff_pf.end > buff_jf.start > buff_pf.start:
                # 破风右端在劲风内
                self._targets_buff_data[target_id]['661_30']['times'][p_pf] = \
                    (buff_pf.start, buff_jf.start - 1, buff_pf.level, buff_pf.layer, buff_pf.src_name)
            elif buff_pf.start < buff_jf.end < buff_pf.end:
                # 破风左侧在劲风内
                self._targets_buff_data[target_id]['661_30']['times'][p_pf] = \
                    (buff_jf.end + 1, buff_pf.end, buff_pf.level, buff_pf.layer, buff_pf.src_name)
            # 指针位移和循环判定终止
            if p_pf < stop_pf and buff_pf.end < buff_jf.start:
                p_pf = min(p_pf + 1, stop_pf)
            elif p_jf < stop_jf and buff_jf.end < buff_pf.start:
                p_jf = min(p_jf + 1, stop_jf)
            # 劲风已到最后一位，破风有剩余的情况
            elif p_jf == stop_jf and buff_jf.end < buff_pf.start:
                end = buff_pf.end
                for i in range(p_pf + 1, stop_pf + 1):
                    buff_pf: buff_res = buff_res(*buff_p_pf[i])
                    self._targets_buff_data[target_id]['661_30']['times'][i] = \
                        (end, buff_pf.end, buff_pf.level, buff_pf.layer, buff_pf.src_name)
                    end = buff_pf.end
                break
            # 破风已到最后一位，劲风有剩余的情况
            elif p_pf == stop_pf and buff_pf.end < buff_jf.start:
                break
            elif p_pf == stop_pf and p_jf == stop_jf:
                break

    def _logic_LiuXue(self):

        # 流血复盘用数据
        # 炼狱技能战斗中无法替换，不会冲突
        LiuXue_GeLie = {29187: 0, 29188: 0, 29186: 1, 29185: 1}  # 子技能id所对应的是否有割裂buff
        GeLie = {13308: 1, 20989: 1}  # 闪刀子技能

        player_data = self._record_info['name_data'].get(self.player_id)
        if not player_data:
            return

        # 状态
        start_blood_time = 0
        latest_blood_time = 0
        has_gelie = 0

        player_talent = player_data.get('aTalent')
        if player_talent:
            LIANYU = 1000 if '炼狱' in player_talent else 2000
        else:
            LIANYU = 2000

        player_name = player_data.get('szName')
        if not player_name:
            player_name = '未知目标'
        # 是否点出了割裂
        # GELIE = 1 if '割裂' in player_talent else 0
        # 流血间隔时间

        for npc_id, blood_data in self._blood_data.items():
            for time, skill_id in blood_data:
                match skill_id:
                    case 8249:
                        # 流血
                        latest_blood_time = time

                    case 13308 | 20989:
                        # 闪刀
                        has_gelie = 1

                    case _:
                        # 斩刀
                        lv_gelie = LiuXue_GeLie.get(skill_id)
                        if lv_gelie is None:
                            continue

                        # 判定流血
                        if has_gelie:
                            if lv_gelie:
                                # 原 -> 割裂，现 -> 割裂：没断
                                continue
                            else:
                                # 原 -> 割裂，现 -> 无割裂：断了
                                buff_lx = buff(8249, 0, 1, latest_blood_time - start_blood_time, player_name)
                                self._add_buff(start_blood_time, player_name, npc_id, buff_lx)
                                start_blood_time = time
                                has_gelie = 0
                        else:
                            if start_blood_time == 0:
                                # 第一个斩刀
                                start_blood_time = time
                                continue

                            else:
                                # 原 -> 无割裂，现 -> 无割裂：根据流血间隔判断
                                if time - latest_blood_time >= LIANYU:
                                    # 断了
                                    # ret.add((start_blood_time, latest_blood_time))
                                    buff_lx = buff(8249, 0, 1, latest_blood_time - start_blood_time, player_name)
                                    self._add_buff(start_blood_time, player_name, npc_id, buff_lx)
                                    start_blood_time = time

            # 全部结束的情况
            if not start_blood_time == 0:
                # ret.add((start_blood_time, latest_blood_time))
                buff_lx = buff(8249, 0, 1, latest_blood_time - start_blood_time, player_name)
                self._add_buff(start_blood_time, player_name, npc_id, buff_lx)






























