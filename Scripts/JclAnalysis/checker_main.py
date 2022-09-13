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
        """
        技能时间轴数据
        :return:
        """
        return self._major_checker.major_skill_list

    @property
    def major_skill_analysis(self):
        """
        重点技能buff覆盖率数据
        :return:
        """
        return self._calc_replay_data()

    @property
    def all_skill_analysis(self):
        """
        所有技能buff数据
        :return:
        """
        return self._calc_all_data()

    @property
    def current_kungfu_skills(self):
        # 当前心法的重点技能
        return self._major_checker.current_kungfu_skills

    @property
    def benefit_buffs(self):
        """
        所有增益buff的生存时间
        :return:
        """
        return self._benefit_checker.benefit_buffs

    def run(self):
        """
        执行技能和增益复盘\n
        :return:
        """
        # 获取生成器对象
        major_gen = self._major_checker.get_work_gen(kungfu=self._attribute.player_kungfu)
        # 非苍云心法的情况下
        if major_gen is None:
            return

        # for loop
        try:
            for skill_id, _ in self._player.skill_events_by_id.items():
                for skill_level, skill_data in _.items():
                    skill_name = skill_data.pop('szName')
                    for msec, cast_state in skill_data.items():
                        # result = cast_state['tResult']
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
        kungfu = self._attribute.player_kungfu

        # 用于计算延迟时间
        for msec, skill_name in operate_data.items():
            if skill_name not in {'盾飞', '盾回', '破', '绝国', '血怒'}:
                times += [(msec, skill_name)]
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

        # 用于豁免部分盾系技能的刀魂和玉简
        # 不分心法也不影响
        times.clear()
        for msec, skill_name in operate_data.items():
            if skill_name not in {'破', '绝国', '血怒'}:
                times += [(msec, skill_name)]
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

        for skill_name, d in skills_data.items():
            # 计算其余
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
                    'nCount': 0,
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
                    'HanJiaCeng': 0,
                    'JianTie': 0,
                    'YuJian': 0,
                    'CanJuan': 0,
                    'DunDang': 0,
                    'Enchant_Belt': 0,
                },
                'Special': {
                    # 特殊记录
                    'count': 0,
                    'norm_rage': [],  # 非特效绝刀怒气
                    'cw_rage': [],  # 特效绝刀怒气
                    'cw_count': 0,  # 特效绝刀数量
                    'jueguo_count': 0,  # 绝国数量
                    'dunfei_rate': 0,  # 盾飞数量/时间
                    'zhenyun_overflow': 0,  # 阵云溢出层数
                    'delay': 0,  # gcd时间
                    'daohun_rate': 0,  # 刀魂盾击占盾回盾击比例
                    'yujian_rate': 0,  # 玉简盾压占盾压比例
                    'hanjia_layer': 0,   # 寒甲平均层数
                    'dundao_1': 0,
                    'dundao_2': 0,
                    'dundao_3': 0,
                    'dundao_4': 0,
                    'duanma_rage': [],
                },
            }
            if not skill_name == '盾飞' and skill_name in delays:
                # 计算平均延迟
                ret['Special']['delay'] = mean(delays[skill_name])
            for time, buffs in d.items():
                # 读取技能数
                ret['Buffs']['nCount'] = len(d)
                # 读取buff
                for key, value in buffs.items():
                    # 对Buffs字段的累加
                    if key in ret['Buffs']:
                        if isinstance(value, bool):
                            # 是否类型
                            if value:
                                ret['Buffs'][key] += 1
                        elif isinstance(value, int):
                            # 层数/等级类型
                            # 寒甲额外适配
                            if key == 'HanJia':
                                if value > 0:
                                    ret['Buffs']['HanJia'] += 1
                                ret['Buffs']['HanJiaCeng'] += value
                            else:
                                ret['Buffs'][key] += value
                    # 对Miss字段的累加
                    # 分心法
                    if kungfu == '分山劲' and not skill_name == '盾飞':
                        match key:
                            case 'DaoHun':
                                if not value:
                                    ret['Miss']['total'] += 1
                                    ret['Miss']['DaoHun'].append(time)
                                if skill_name == '盾击' and value:
                                    ret['Special']['daohun_rate'] += 1
                            case 'FenYe':
                                if not value:
                                    ret['Miss']['total'] += 1
                                    ret['Miss']['FenYe'].append(time)
                            case 'XueNu':
                                if value < 2:
                                    ret['Miss']['total'] += 1
                                    ret['Miss']['XueNu'].append(time)
                            case 'YuJian' if has_yujian:
                                if skill_name in {'盾击', '盾压'}:
                                    # 飞击飞压
                                    if value < 6:
                                        ret['Miss']['total'] += 1
                                        ret['Miss']['YuJian'].append(time)
                            case '阵云结晦' | '月照连营' | '雁门迢递':
                                # 6层阵云
                                if value < 6:
                                    ret['Miss']['total'] += 1
                                    ret['Miss']['YuJian'].append(time)

                    elif kungfu == '铁骨衣':
                        pass

                    # 对Special字段的累加
                    match key:
                        case 'norm_rage':
                            ret['Special']['norm_rage'].append(value)
                        case 'cw_rage':
                            ret['Special']['cw_rage'].append(value)
                        case 'cw':
                            if value:
                                ret['Special']['cw_count'] += 1
                        case 'jueguo':
                            ret['Special']['jueguo_count'] += value
                        case 'ZhenYun_Overflow':
                            ret['Special']['zhenyun_overflow'] += len(value)
                            ret['Miss']['total'] += len(value)
                            ret['Miss']['ZhenYun'] += value
                        case 'stage':
                            if f'dundao_{value}' in ret['Special']:
                                ret['Special'][f'dundao_{value}'] += 1
                        case 'rage':
                            ret['Special']['duanma_rage'].append(value)

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

                            if _min_index is not None:
                                _ms['total'] = max(0, _ms['total'] - 1)
                                _ms[k].pop(_min_index)

        # 检查是否有关键技能未在返回值中
        for import_skill in self._major_checker.current_kungfu_skills:
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
                'nCount': 0,
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
                'HanJiaCeng': 0,
                'JianTie': 0,
                'YuJian': 0,
                'CanJuan': 0,
                'DunDang': 0,
                'Enchant_Belt': 0,
            },
            'Special': {
                # 特殊记录
                'count': 0,
                'norm_rage': [],  # 非特效绝刀怒气
                'cw_rage': [],  # 特效绝刀怒气
                'cw_count': 0,  # 特效绝刀数量
                'jueguo_count': 0,  # 绝国数量
                'dunfei_rate': 0,  # 盾飞数量/时间
                'zhenyun_overflow': 0,  # 阵云溢出层数
                'delay': 0,  # gcd时间
                'daohun_rate': 0,  # 刀魂盾击占盾回盾击比例
                'yujian_rate': 0,  # 玉简盾压占盾压比例
                'hanjia_layer': 0,  # 寒甲平均层数
                'dundao_1': 0,
                'dundao_2': 0,
                'dundao_3': 0,
                'dundao_4': 0,
                'duanma_rage': 0,
            },
        }
            if import_skill not in ret_value:
                ret_value[import_skill] = ret

        # 计算覆盖率
        for sk, d in ret_value.items():
            _n = d['Buffs'].pop('nCount')
            ret_value[sk]['Special']['count'] = _n
            if _n <= 0:
                continue
            for k, v in d['Buffs'].items():
                ret_value[sk]['Buffs'][k] = v / _n
            # 计算特殊数据平均值
            match sk:
                case '绝刀':
                    ret_value[sk]['Special']['norm_rage'] = np.mean(ret_value[sk]['Special']['norm_rage'])
                    ret_value[sk]['Special']['cw_rage'] = np.mean(ret_value[sk]['Special']['cw_rage'])
            # elif sk == '阵云结晦':
            #     ret_value[sk]['Special']['']
                case '盾飞':
                    df_t, df_c = self._player.dunfei_time_and_count
                    if df_t > 0:
                        # 每次盾飞减去一次盾飞次数计数
                        ret_value[sk]['Special']['dunfei_rate'] = (_n - df_c) / (df_t / 1000)
                    else:
                        pass
                case '雁门迢递':
                    ret_value[sk]['Special']['jueguo_count'] = ret_value[sk]['Special']['jueguo_count'] / _n
                case '盾击':
                    if dunhui_count > 0 and kungfu == '分山劲':
                        ret_value[sk]['Special']['daohun_rate'] = ret_value[sk]['Special']['daohun_rate'] / dunhui_count
                case '盾压':
                    if kungfu == '分山劲':
                        ret_value[sk]['Special']['yujian_rate'] = ret_value[sk]['Buffs']['YuJian'] / 6
                case '断马摧城':
                    ret_value[sk]['Special']['duanma_rage'] = np.mean(ret_value[sk]['Special']['duanma_rage'])

            # 寒甲层数
            if kungfu == '铁骨衣':
                if not sk == '盾挡':
                    ret_value[sk]['Special']['hanjia_layer'] = ret_value[sk]['Buffs']['HanJiaCeng']




        return ret_value

    def _calc_all_data(self):
        """
        整理all_skills_list: 将时间轴上的技能绑定上buff
        :return:
        """
        data = self._major_checker.all_skill_analysis
        # 把data里的buff添加到operate_list中
        operate_list = self.operate_skill_list

        # 破招单独处理
        _pozhao_lst = None

        # 需要额外删除的技能
        _del = []
        # 1. 遍历技能轴，读取并写入非破招的buff
        for msec, skill_name in operate_list.items():
            if not skill_name == '破':
                if skill_name in data:
                    # 读取出所有该技能的施放时间, 选择最近的一个
                    _release_times = sorted(data[skill_name].keys())
                    for _release_time in _release_times:
                        if (_release_time - msec) < 1000:
                            buff_data = data[skill_name].pop(_release_time)
                            # 重写原数据
                            operate_list[msec] = {'name': skill_name, 'buffs': buff_data}
                            break
                    # 未知技能的情况
                    else:
                        _del.append(msec)
                else:
                    operate_list[msec] = {'name': skill_name, 'buffs': None}
            else:
                if _pozhao_lst is None:
                    _pozhao_lst = [msec]
                else:
                    _pozhao_lst.append(msec)
                _del.append(msec)

        # 2. 替换技能轴中破招数据
        # 先删除原数据
        for msec in _del:
            del operate_list[msec]
        _total = None
        _group = []
        latest_pozhao_time = None
        for msec in _pozhao_lst:
            # 分割破招轴
            # 开始的情况
            if latest_pozhao_time is None:
                latest_pozhao_time = msec
                _group.append(latest_pozhao_time)
            # 同一个破招的情况
            elif msec - latest_pozhao_time < 100:
                _group.append(latest_pozhao_time)
            # 不同破招的情况
            else:
                if _total is None:
                    _total = [[i for i in _group]]
                else:
                    _total.append([i for i in _group])
                _group.clear()
        for group in _group:
            for msec in group:
                if msec not in operate_list:
                    operate_list[msec] = {'name': '破', 'buffs': None}
                    break

        # 3. 排序
        ret_value = {}
        for time in sorted(operate_list.keys()):
            ret_value[time] = operate_list[time]

        return ret_value

    def run_buff(self):
        """
        统计每一个buff的存在情况和作用的技能
        :return:
        """
        self._benefit_checker.check_benefit_buff(self._player.buff_data)






