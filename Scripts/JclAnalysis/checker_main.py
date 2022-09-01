# coding: utf-8
# author: LinXin
# 从skill_event_by_id中提取技能轴和增益数据, 并将技能轴数据提交给评分模块

from typing import Dict

import numpy as np
from numpy import mean

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

    @property
    def operate_skill_list(self):
        return self._major_checker.major_skill_list

    @property
    def major_skill_analysis(self):
        return self._calc_replay_data()

    @property
    def current_kungfu_skills(self):
        return self._major_checker.current_kungfu_skills

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
                        _type = cast_state['nType']
                        # 发送内容
                        major_gen.send((_type, msec, skill_id, skill_level, skill_name, buff))
        # try:
        finally:
            major_gen.close()
            # print(*[f"{i}: {self._major_checker.major_skill_list[i]}\n" for i in sorted(self._major_checker.major_skill_list.keys())])
            # print(self._major_checker.major_skill_analysis)
        # except StopIteration:
        #     pass

    def _calc_replay_data(self):
        """
        整理major_skill_analysis, operate_skill_list
        :return:
        """
        ret_value = {}
        times = []
        delays = {}
        release = {}
        skills_data = self._major_checker.major_skill_analysis
        operate_data = self.operate_skill_list
        has_yujian = self._attribute.yunshan_enchant
        # 用于计算延迟时间
        for msec, skill_name in operate_data.items():
            if skill_name not in {'盾飞', '盾回', '破', '绝国', '血怒'}:
                times += [(msec, skill_name)]
        del msec, skill_name
        times = sorted(times, key=lambda i: i[0])
        for index, time in enumerate(times):
            if index < len(times) - 1:
                delay = times[index+1][0] - time[0]
                if delay > 3000:
                    # 过滤掉大于2~3个gcd的情况
                    continue
                if time[1] in delays:
                    delays[time[1]].append(delay)
                else:
                    delays[time[1]] = [delay]
        del index, time

        # 用于豁免部分盾系技能的刀魂和玉简
        times.clear()
        for msec, skill_name in operate_data.items():
            if skill_name not in {'破', '绝国', '血怒'}:
                times += [(msec, skill_name)]
        del msec, skill_name
        times = sorted(times, key=lambda i: i[0])
        # 用于豁免第一个斩刀和绝刀
        rel_zd = True
        rel_jd = True
        # 用于计算刀魂盾击比例
        dunhui_count = 0
        for index, tm in enumerate(times):
            if index == 0:
                # 全部豁免权
                release[tm[1]] = {tm[0]: {'DaoHun', 'FenYe', 'XueNu', 'YuJian'}}
            elif rel_jd and tm[1] == '绝刀':
                release[tm[1]] = {tm[0]: {'FenYe'}}
                rel_jd = False
            elif rel_zd and tm[1] == '斩刀':
                release[tm[1]] = {tm[0]: {'FenYe'}}
                rel_zd = False
            elif tm[1] in {'盾击', '盾压'}:
                # 刀魂玉简部分豁免
                if times[index-1][1] == '盾回':
                    _rel = {'YuJian'}
                    # 保证盾回后必须有技能
                    dunhui_count += 1
                elif times[min(index+2, len(times)-1)][1] not in {'盾击', '盾压'} and times[index+1][1] == '盾飞' or times[index-1][1] == '盾飞':
                    _rel = {'DaoHun'}
                else:
                    _rel = {'DaoHun', 'YuJian'}
                if tm[1] in release:
                    release[tm[1]].update({tm[0]: _rel})
                else:
                    release[tm[1]] = {tm[0]: _rel}
        del index, tm, _rel, rel_jd, rel_zd

        # 计算其余
        for skill_name, d in skills_data.items():
            ret = {
                # 'Count': {},
                'Miss': {
                    # 失误时间点和次数
                    'total': 0,
                    'DaoHun': [],
                    'FenYe': [],
                    'XueNu': [],
                    'YuJian': [],
                    'ZhenYun': []
                },
                'Buffs': {
                    # 覆盖率和平均期望
                    'nCount': len(d),
                    'DaoHun': 0,
                    'FenYe': 0,
                    'CongRong': 0,
                    'FengMing': 0,
                    'ChongYun': 0,
                    'JunXiao': 0,
                    'Enchant_Hat': 0,
                    'XueNu': 0,
                    'LianZhan': 0,
                    'HanJia': 0,
                    'JianTie': 0,
                    'YuJian': 0,
                    'CanJuan': 0,
                    'DunDang': 0,
                    'Enchant_Belt': 0,
                },
                'Special': {
                    # 特殊记录
                    'norm_rage': [],     # 非特效绝刀怒气
                    'cw_rage': [],       # 特效绝刀怒气
                    'cw_count': 0,      # 特效绝刀数量
                    'jueguo_count': 0,  # 绝国数量
                    'dunfei_rate': 0,   # 盾飞数量/时间
                    'zhenyun_overflow': 0,  # 阵云溢出层数
                    'delay': 0,          # gcd时间
                    'daohun_rate': 0,   # 刀魂盾击占盾回盾击比例
                    'yujian_rate': 0,   # 玉简盾压占盾压比例
                },
            }
            if not skill_name == '盾飞' and skill_name in delays:
                ret['Special']['delay'] = mean(delays[skill_name])
            for time, buffs in d.items():
                for key, value in buffs.items():
                    if key in ret['Buffs']:
                        if isinstance(value, bool):
                            # 是否类型
                            if value:
                                ret['Buffs'][key] += 1
                        elif isinstance(value, int):
                            # 层数/等级类型
                            ret['Buffs'][key] += value
                    # 检测失误
                    # 'Miss': {
                    #     'total': [],
                    #     'DaoHun': [],
                    #     'FenYe': [],
                    #     'XueNu': [],
                    #     'YuJian': [],
                    # },
                    if not skill_name == '盾飞':
                        if key == 'DaoHun':
                            if not value:
                                ret['Miss']['total'] += 1
                                ret['Miss']['DaoHun'].append(time)
                            if skill_name == '盾击' and value:
                                ret['Special']['daohun_rate'] += 1
                        elif key == 'FenYe':
                            if not value:
                                ret['Miss']['total'] += 1
                                ret['Miss']['FenYe'].append(time)
                        elif key == 'XueNu':
                            if value < 2:
                                ret['Miss']['total'] += 1
                                ret['Miss']['XueNu'].append(time)
                        elif key == 'YuJian' and has_yujian:
                            if skill_name in {'盾击', '盾压'}:
                                # 飞击飞压
                                if value < 6:
                                    ret['Miss']['total'] += 1
                                    ret['Miss']['YuJian'].append(time)
                            elif skill_name in {'阵云结晦', '月照连营', '雁门迢递'}:
                                # 6层阵云
                                if value < 6:
                                    ret['Miss']['total'] += 1
                                    ret['Miss']['YuJian'].append(time)

                    # 额外
                    # 'Special': {
                    #     'rage': 0,
                    #     'jueguo': 0,
                    # }
                    # 绝刀特殊字段
                    # buff_ret['norm_rage'] = 0
                    # buff_ret['cw_rage'] = 0
                    # buff_ret['cw'] = False
                    # buff_ret['ZhenYun_Overflow'] = False
                    # 雁门特殊字段
                    # buff_ret['jueguo'] = 0
                    if key == 'norm_rage':
                        ret['Special']['norm_rage'].append(value)
                    elif key == 'cw_rage':
                        ret['Special']['cw_rage'].append(value)
                    elif key == 'cw':
                        if value:
                            ret['Special']['cw_count'] += 1
                    elif key == 'jueguo':
                        ret['Special']['jueguo_count'] += value
                    elif key == 'ZhenYun_Overflow':
                        ret['Special']['zhenyun_overflow'] += len(value)
                        ret['Miss']['total'] += len(value)
                        ret['Miss']['ZhenYun'] += value

            ret_value[skill_name] = ret
        # 技能豁免事件
        for sk_name, d in release.items():
            for tar_msec, _rel in d.items():
                if sk_name in ret_value:
                    _ms = ret_value[sk_name]['Miss']
                    for k in _rel:
                        if len(_ms[k]) > 0:
                            _min_index = None
                            _min_range = None
                            for idx, miss_msec in enumerate(_ms[k]):
                                _range = abs(miss_msec - tar_msec)
                                if _range < 1000:
                                    if _min_range is None or _min_range > _range:
                                        _min_index = idx
                                        _min_range = _range

                            del idx, miss_msec, _range
                            if _min_index is not None:
                                _ms['total'] = max(0, _ms['total'] - 1)
                                _ms[k].pop(_min_index)
                            del _min_index, _min_range
                    del k
                    del _ms
            del tar_msec, _rel
        del sk_name, d

        # 计算覆盖率
        for sk, d in ret_value.items():
            _n = d['Buffs'].pop('nCount')
            ret_value[sk]['Special']['count'] = _n
            if _n <= 0:
                continue
            for k, v in d['Buffs'].items():
                ret_value[sk]['Buffs'][k] = v / _n
            # 计算特殊数据平均值
            if sk == '绝刀':
                ret_value[sk]['Special']['norm_rage'] = np.mean(ret_value[sk]['Special']['norm_rage'])
                ret_value[sk]['Special']['cw_rage'] = np.mean(ret_value[sk]['Special']['cw_rage'])
            # elif sk == '阵云结晦':
            #     ret_value[sk]['Special']['']
            elif sk == '盾飞':
                df_t, df_c = self._player.dunfei_time_and_count
                if df_t > 0:
                    # 每次盾飞减去一次盾飞次数计数
                    ret_value[sk]['Special']['dunfei_rate'] = (_n - df_c) / (df_t / 1000)
                else:
                    pass
            elif sk == '雁门迢递':
                ret_value[sk]['Special']['jueguo_count'] = ret_value[sk]['Special']['jueguo_count'] / _n
            elif sk == '盾击':
                if dunhui_count > 0:
                    ret_value[sk]['Special']['daohun_rate'] = ret_value[sk]['Special']['daohun_rate'] / dunhui_count
            elif sk == '盾压':
                ret_value[sk]['Special']['yujian_rate'] = ret_value[sk]['Buffs']['YuJian'] / 6

        return ret_value








