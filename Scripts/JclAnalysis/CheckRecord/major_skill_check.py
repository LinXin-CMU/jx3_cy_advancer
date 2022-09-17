# coding: utf-8
# author: LinXin
# 主要技能的类型检查
# 分山: 阵云*3, 绝国, 斩刀, 绝刀, 盾击, 盾飞
# 铁骨: 盾刀, 盾击, 盾压, 流血, 斩刀, 绝刀, 劫刀, 断马

from typing import Dict

from CustomClasses.TypeHints import Attribute
from Scripts.Config.config import ConfigSetting
from Sources.Jx3_Datas.Files.jx3_skill import skill
from Sources.Jx3_Datas.Files.get_other_data import get_buff_or_skill_from_jx3box


class MajorSkillChecker:

    def __init__(self):
        self._major_skills_result = {}
        self._major_skills_list = {}
        self._all_skills_result = {}
        self.config = ConfigSetting()
        self._current_kungfu_skills = None

    @property
    def major_skill_list(self):
        return self._major_skills_list

    @property
    def major_skill_analysis(self):
        return self._major_skills_result

    @property
    def all_skill_analysis(self):
        return self._all_skills_result

    @property
    def current_kungfu_skills(self):
        return self._current_kungfu_skills


    def get_work_gen(self, kungfu: str) -> callable:
        """
        外层接口\n
        :return:
        """
        # 判断心法
        if kungfu == '分山劲':
            gen = self._check_fen_shan_skill()
            self._current_kungfu_skills = ['阵云结晦', '月照连营', '雁门迢递', '盾飞', '斩刀', '绝刀', '盾击', '盾压']
        elif kungfu == '铁骨衣':
            gen = self._check_tie_gu_skill()
            self._current_kungfu_skills = ['盾刀', '盾击', '盾压', '盾飞', '斩刀', '绝刀', '盾挡', '断马摧城']
        else:
            return None
        gen.send(None)
        return gen

    def _check_fen_shan_skill(self):
        """
        检查分山技能: 阵云*3, 斩刀, 绝刀, 盾击, 盾压, 盾飞\n
        :return:
        """
        alls = {'阵云结晦', '月照连营', '雁门迢递', '断马摧城', '斩刀', '绝刀', '劫刀', '闪刀', '盾毅', '撼地', '盾舞', '隐刀', '血刀', '盾击', '盾压', '盾刀', '盾猛', '盾飞', '破'}
        player_skills = set()
        not_player_skills = set()
        zhenyun_max_layer = int(self.config['zhenyun_max_layer'])
        zhenyun_overflow = None
        # last_msec = None
        self._major_skills_result = {}
        self._major_skills_list = {}
        self._all_skills_result = {}

        while True:
            # 获取数据
            _type, msec, skill_id, skill_level, skill_name, buff_data = yield
            # 终止符
            if not skill_name:
                break
            # 过滤盾击aoe
            if skill_id in {24102, 24103}:
                continue
            # 针对重点技能的分析
            # 这里针对的是伤害子技能
            if _type == 'damage':
                if skill_name in alls or skill_id == 13040:
                    buff_ret = {}
                    if not skill_id == 13040:
                        buff_ret = self._check_basic_buff(buff_data)
                    # 记录时间
                    # 放到外层
                    # if last_msec is not None:
                    #     buff_ret['Delay'] = msec - last_msec
                    # last_msec = msec
                    match skill_name:
                        case '绝刀':
                            buff_ret['norm_rage'] = 0
                            buff_ret['cw_rage'] = 0
                            buff_ret['cw'] = False
                            # 橙武特效标记
                            if 8474 in buff_data:
                                buff_ret['cw'] = True
                                # 绝刀怒气
                            if 9052 in buff_data:
                                # 存在绝刀怒气判定buff的情况
                                _lv = buff_data[9052][0]
                                if _lv > 4:
                                    _lv = _lv - 4
                                if buff_ret['cw']:
                                    buff_ret['cw_rage'] = (_lv + 1) * 10
                                else:
                                    buff_ret['norm_rage'] = (_lv + 1) * 10
                            # 阵云溢出检测
                            if 22993 in buff_data:
                                if buff_data[22993][1] >= zhenyun_max_layer:
                                    if zhenyun_overflow is None:
                                        zhenyun_overflow = [msec]
                                    else:
                                        zhenyun_overflow.append(msec)
                            else:
                                # 绝刀速度太快导致不存在buff的情况
                                pass
                                # 暂无好的处理方案
                        case '血怒':
                            if 22993 in buff_data:
                                if buff_data[22993][1] >= zhenyun_max_layer:
                                    if zhenyun_overflow is None:
                                        zhenyun_overflow = [msec]
                                    else:
                                        zhenyun_overflow.append(msec)
                        case '阵云结晦':
                            # # 阵云溢出
                            # if 22993 in buff_data:
                            #     if buff_data[22993][1] >= zhenyun_max_layer:
                            #         buff_ret['ZhenYun_Overflow'] = True
                            if zhenyun_overflow is None:
                                buff_ret['ZhenYun_Overflow'] = []
                            else:
                                buff_ret['ZhenYun_Overflow'] = zhenyun_overflow
                                zhenyun_overflow = None
                            pass
                        case '雁门迢递':
                            buff_ret['jueguo'] = 0
                            if 22979 in buff_data:
                                buff_ret['jueguo'] = buff_data[22979][0] - 1
                            else:
                                pass
                                # 还未发现的情况
                    imports = {'阵云结晦', '月照连营', '雁门迢递', '斩刀', '绝刀', '盾击', '盾压', '盾飞'}
                    if skill_name in imports:
                        if skill_name not in self._major_skills_result:
                            self._major_skills_result[skill_name] = {msec: buff_ret}
                        else:
                            self._major_skills_result[skill_name][msec] = buff_ret

                    if skill_name not in self._all_skills_result:
                        self._all_skills_result[skill_name] = {msec: buff_ret}
                    else:
                        self._all_skills_result[skill_name][msec] = buff_ret
            # 计算延迟的技能轴
            # 利用母技能判断
            if (skill_id, skill_level) not in not_player_skills:
                if (skill_id, skill_level) not in player_skills:
                    # 查询
                    try:
                        _kf = skill[skill_id][skill_level]['BelongKungfu']
                    except KeyError:
                        try:
                            _kf = get_buff_or_skill_from_jx3box('skill', skill_id, skill_level)['BelongKungfu']
                        except KeyError:
                            # 访问不到时直接跳过
                            continue
                    if skill_id in {30769, 30855, 30856, 9003, 9004, 9005, 9006, 9007} or _kf in {'10385', '10386', '10384', '10383', '24785'} \
                            and skill_name not in {'阵云绝', '破招外功伤害子技能（母）'}:
                        # 阵云单独处理
                        # 小轻功单独处理
                        # 苍云套路+破招
                        player_skills.add((skill_id, skill_level))
                        self._major_skills_list[msec] = skill_name
                    else:
                        not_player_skills.add((skill_id, skill_level))
                else:
                    self._major_skills_list[msec] = skill_name

    def _check_tie_gu_skill(self):
        """
        检查铁骨技能: 盾刀, 盾击, 盾压, 流血, 斩刀, 绝刀, 劫刀, 断马摧城\n
        :return:
        """
        imports = {'盾刀', '盾击', '盾压', '盾飞', '斩刀', '绝刀', '盾挡', '断马摧城', '破'}
        player_skills = set()
        not_player_skills = set()
        # 盾刀id
        dundao_id = {
            13044: 1,
            13244: 2,
            13060: 3,
            13119: 4
        }
        # 返回值
        self._major_skills_result = {}
        self._major_skills_list = {}
        self._all_skills_result = {}
        while True:
            # 获取数据
            _type, msec, skill_id, skill_level, skill_name, buff_data = yield
            # 针对重点技能的分析
            # 这里针对的是伤害子技能
            if _type == 'damage' or skill_id == 13391:
                if skill_name in imports:
                    # buff_ret = {}
                    buff_ret = self._check_basic_buff(buff_data)
                    # 记录时间
                    # 放到外层
                    match skill_name:
                        case '盾刀':
                            buff_ret['stage'] = 0
                            if skill_id in dundao_id:
                                buff_ret['stage'] = dundao_id[skill_id]
                            # 盾刀段数1-4
                            # 寒甲平均层数
                        case '盾击':
                            pass
                            # cd利用率
                            # 寒甲平均层数
                        case '盾压':
                            # 重置率
                            # 寒甲平均层数
                            pass
                        case '盾飞':
                            # 时间比例
                            # 寒甲平均层数
                            pass
                        case '斩刀':
                            # 寒甲平均层数
                            pass
                        case '绝刀':
                            # 非特效平均怒气
                            buff_ret['norm_rage'] = 0
                            buff_ret['cw'] = False
                            # 橙武特效标记
                            if 8474 in buff_data:
                                buff_ret['cw'] = True
                                # 绝刀怒气
                            if 9052 in buff_data:
                                # 存在绝刀怒气判定buff的情况
                                _lv = buff_data[9052][0]
                                if _lv > 4:
                                    _lv = _lv - 4
                                if not buff_ret['cw']:
                                    buff_ret['norm_rage'] = (_lv + 1) * 10
                            # 特效绝刀数量
                            # 寒甲平均层数
                            pass
                        case '盾挡':
                            # 卡gcd释放占比
                            # 平均怒气
                            pass
                        case '断马摧城':
                            # print(skill_level)  # level=1-12
                            # 寒甲平均层数
                            # 平均怒气
                            buff_ret['rage'] = (skill_level - 1) * 10
                            # 卡gcd释放占比
                            pass
                    if skill_name not in self._major_skills_result and not skill_name == '破':
                        self._major_skills_result[skill_name] = {msec: buff_ret}
                    elif not skill_name == '破':
                        self._major_skills_result[skill_name][msec] = buff_ret
                    if skill_name not in self._all_skills_result:
                        self._all_skills_result[skill_name] = {msec: buff_ret}
                    else:
                        self._all_skills_result[skill_name][msec] = buff_ret

            if (skill_id, skill_level) not in not_player_skills:
                if (skill_id, skill_level) not in player_skills:
                    # 查询
                    try:
                        _kf = skill[skill_id][skill_level]['BelongKungfu']
                    except KeyError:
                        _kf = get_buff_or_skill_from_jx3box('skill', skill_id, skill_level)['BelongKungfu']
                    if _kf in {'10385', '10386', '10384', '10383', '24785'} and skill_name not in {'破招外功伤害子技能（母）'}:
                        # 苍云套路+破招
                        player_skills.add((skill_id, skill_level))
                        self._major_skills_list[msec] = skill_name
                    else:
                        not_player_skills.add((skill_id, skill_level))
                else:
                    self._major_skills_list[msec] = skill_name



    @staticmethod
    def _check_basic_buff(buff_data):
        ret = {
            'DaoHun': False,
            'FenYe': False,
            'CongRong': False,
            'FengMing': False,
            'ChongYun': False,
            'JunXiao': False,
            'Enchant_Hat': False,
            'XueNu': 0,
            'LianZhan': 0,
            'HanJia': 0,
            'JianTie': 0,
            'YuJian': 0,
            'CanJuan': 0,
            'DunDang': 0,
            'Enchant_Belt': 0,
            }
        _ishave_mapping = {
            8627: 'DaoHun',
            17176: 'FenYe',
            8423: 'CongRong',
            14309: 'FengMing',
            14964: 'ChongYun',
            1428: 'JunXiao',
            15413: 'Enchant_Hat'
        }
        _islayer_mapping = {
            8244: 'XueNu',
            8385: 'XueNu',
            8386: 'XueNu',
            8267: 'LianZhan',
            8271: 'HanJia',
            8272: 'JianTie',
            21648: 'YuJian',
            21651: 'CanJuan'
        }
        _islevel_mapping = {
            8448: 'DunDang',
            15455: 'Enchant_Belt'
        }

        for _id, _key in _ishave_mapping.items():
            if _id in buff_data:
                ret[_key] = True
        for _id, _key in _islayer_mapping.items():
            if _id in buff_data:
                ret[_key] += buff_data[_id][1]
        for _id, _key in _islevel_mapping.items():
            if _id in buff_data:
                ret[_key] += buff_data[_id][0]

        # 大寒甲特殊处理
        if 17772 in buff_data:
            ret['HanJia'] += buff_data[17772][1] * 100

        return ret
















