# coding: utf-8
# author: LinXin
from typing import Dict, List, Union
from numpy import mean

total_damage = 0


def _check_damages(tResult: Dict, new_result: Dict, *, critical=0, msec=None):
    """
    用于更新技能效果的函数
    :param tResult:
    :param new_result:
    :param critical:
    :return tResult:
    """
    global total_damage
    # 新内容检测
    if len(tResult) == 0:
        tResult = {
            'normal': [],
            'critical': [],
            'normal_time': [],
            'critical_time': []
        }
    # 判断类型添加伤害
    if '有效伤害' in new_result:
        dmg = new_result['有效伤害']
        total_damage += dmg
        if critical:
            if tResult['critical'] is None:
                tResult['critical'] = [dmg]
                tResult['critical_time'] = [msec]
            else:
                tResult['critical'].append(dmg)
                tResult['critical_time'].append(msec)
        else:
            if tResult['normal'] is None:
                tResult['normal'] = [dmg]
                tResult['normal_time'] = [msec]
            else:
                tResult['normal'].append(dmg)
                tResult['normal_time'].append(msec)

    return tResult


def _reshape_to_table(data: Dict[int, Dict[str, Union[str, int, Dict[str, Union[str, int, Dict]]]]],
                      id_to_name_dict: Dict[int, Dict[str, str]]):
    """
    将Player._skill整理成可录入表格的格式，
    合并同名技能，拆分等级技能，整理技能数据\n
    :type id_to_name_dict: object
    :param data: _skill_event_by_time，按时间分类的数据
    :return _skill:
    """

    # 1. 确定要展示的内容
    # 技能名，技能次数，伤害量，比重
    # 未会心率，未会心伤害（最大，最小，平均），伤害占比
    # 会心率，会心伤害（最大，最小，平均），伤害占比
    # 一个按id统计的结构即为
    # _skill = {
    #     'szName': str: {
    #         等级已被合并或拆分
    #         'dwID': set,
    #         'nCount': int,
    #         'nCritical': int,
    #         'nDodge': int,
    #         '_now_result': {
    #             'normal': List,
    #             'critical': List
    #         },
    #         'tResult': {
    #             伤害类型已s被合并
    #             'normal': {msec: dmg},
    #             'critical': {msec: dmg},
    #         },
    #         'result_final': {
    #             'normal': {
    #                 'max': int,
    #                 'min': int,
    #                 'mean': int,
    #             },
    #             'critical': {
    #                 'max': int,
    #                 'min': int,
    #                 'mean': int,
    #             },
    #             'dodge': int,
    #             'total': int
    #         },
    #         'percentage': {
    #             'total': float,
    #             'critical': float,
    #             'dodge': float,
    #         },
    #         'targets': {
    #             'target1': {
    #                   'normal': {
    #                       'max', 'min', 'mean', 'nCount'
    #                   },
    #                    'critical': {
    #                        'max', 'min', 'mean', 'nCount'
    #                   },
    #                    'dodge': {
    #                        0, 0, 0, 'nCount'
    #                   }
    #             },
    #             'target2': ...
    #         }
    #     }
    # }
    # 返回值
    _skill = {}
    # 计算占比用
    global total_damage

    for target, tar_data in data.items():
        # 记录用
        try:
            target_name: str = id_to_name_dict[target]['szName']
        except KeyError:
            target_name = "未知目标"
        for msec, skill_datas in tar_data.items():
            # 每个技能的dict
            for msec_index, skill_data in skill_datas.items():
                skill_name = skill_data['szName']
                skill_id = skill_data['dwID']
                # skill_level = skill_data['dwLevel']
                # 会心判断
                if skill_data['bCritical'] == '会心':
                    _critical = 1
                else:
                    _critical = 0
                # 闪避判断
                if 'dodge' in skill_data['tResult']:
                    _dodge = 1
                else:
                    _dodge = 0
                # 伤害筛选
                _dmg = skill_data['tResult']

                if '有效伤害' not in _dmg or _dmg['有效伤害'] == 0:
                    if 'dodge' not in _dmg:
                        continue

                # 统计数据
                if skill_name in _skill:
                    _sk = _skill[skill_name]
                    _sk['dwID'].add(skill_id)
                    _sk['nCount'] += 1
                    _sk['nCritical'] += _critical
                    # 先存到一个local地址，待当前目标统计完再加入到总记录nDodge
                    _sk['_now_dodge'] += _dodge
                    # 先存到一个local地址，待当前目标统计完再加入到总记录tResult
                    _sk['_now_result'] = _check_damages(_sk['_now_result'], skill_data['tResult'], critical=_critical, msec=msec)
                    _sk['_now_target'].update({msec: target_name})
                else:
                    _skill[skill_name] = {
                        'dwID': {skill_id},
                        'nCount': 1,
                        'nCritical': _critical,
                        'nDodge': 0,
                        '_now_dodge': _dodge,
                        '_now_result': _check_damages({}, skill_data['tResult'], critical=_critical, msec=msec),
                        '_now_target': {msec: target_name},
                        'tResult': {'normal': dict(), 'critical': dict()},
                        'targets': dict()
                    }
            # 分目标统计的部分
        for skill_name, skill_count in _skill.items():
            # 取出当前数据
            _normals = skill_count['_now_result']['normal']
            _normal_check = 0
            if _normals is None or _normals == []:
                _normals = [0]
                # 无数据时计数-1，因为这里填入了一个默认的0
                _normal_check = 1
            _criticals = skill_count['_now_result']['critical']
            _critical_check = 0
            if _criticals is None or _criticals == []:
                _criticals = [0]
                _critical_check = 1
            # 计入到技能数据中
            # try:
            #     target_name: str = id_to_name_dict[target]['szName']
            # except KeyError:
            #     target_name = "未知目标"
            _skill[skill_name]['targets'][target] = {
                'target_name': target_name,
                'total': sum(_normals) + sum(_criticals),
                'normal': {
                    'max': max(_normals), 'min': min(_normals), 'mean': int(mean(_normals)), 'nCount': len(_normals)-_normal_check
                },
                'critical': {
                    'max': max(_criticals), 'min': min(_criticals), 'mean': int(mean(_criticals)), 'nCount': len(_criticals)-_critical_check
                },
                'dodge': {
                    'max': 0, 'min': 0, 'mean': 0, 'nCount': _skill[skill_name]['_now_dodge']
                }
            }
            # 清空0记录
            if _normals == [0]:
                _normals = []
            if _criticals == [0]:
                _criticals = []

            # 将当前记录加入到总记录中
            _skill[skill_name]['tResult']['normal'].update(zip(_skill[skill_name]['_now_result']['normal_time'], _skill[skill_name]['_now_result']['normal']))
            _skill[skill_name]['tResult']['critical'].update(zip(_skill[skill_name]['_now_result']['critical_time'], _skill[skill_name]['_now_result']['critical']))
            _skill[skill_name]['nDodge'] += _skill[skill_name]['_now_dodge']
            # 清空当前
            # _skill[skill_name]['_now_result']['normal'] = []
            # _skill[skill_name]['_now_result']['critical'] = []
            for key in _skill[skill_name]['_now_result']:
                _skill[skill_name]['_now_result'][key] = []
            _skill[skill_name]['_now_dodge'] = 0


    for skill_name, skill_count in _skill.items():
        # 统计极大值，极小值，平均值
        _normals = list(skill_count['tResult']['normal'].values())
        if _normals is None or len(_normals) == 0:
            _normals = [0]
        _criticals = list(skill_count['tResult']['critical'].values())
        if _criticals is None or len(_criticals) == 0:
            _criticals = [0]
        _skill[skill_name]['result_final'] = {
            'normal': {
                'max': max(_normals),
                'min': min(_normals),
                'mean': int(mean(_normals))
            },
            'critical': {
                'max': max(_criticals),
                'min': min(_criticals),
                'mean': int(mean(_criticals))
            },
            'dodge': {
                'max': 0,
                'min': 0,
                'mean': 0
            },
            'total': sum(_normals) + sum(_criticals)
        }
        # 计算占比
        _skill[skill_name]['percentage'] = {
            'total': (sum(_normals) + sum(_criticals)) / total_damage,
            'critical': skill_count['nCritical'] / skill_count['nCount'],
            'dodge': skill_count['nDodge'] / skill_count['nCount']
        }
    return _skill


def read_origin_skill_data(data: Dict[int, Dict[str, Union[int, Dict]]], id_to_name_dict: Dict[int, Dict[str, str]]):
    # 按id统计
    # self._skill_event_by_time[msc] = {
    #     "dwID": skill_id,
    #       分类依据
    #     "dwLevel": skill_level,
    #       分类依据
    #     "bCritical": data['bCriticalStrike'],
    #       统计次数
    #     "tResult": data['tResultCount'],
    #       累加
    #     "tBuffs": {buff_id: (buff_data[1], buff_data[2]) for buff_id, buff_data in self._waiting_buffs.items()}
    #       分类并统计
    # }
    # 清空统计
    global total_damage
    total_damage = 0
    # 整理表格格式的技能统计
    data_to_table = _reshape_to_table(data, id_to_name_dict)
    # 计算流血时间轴
    # _read_blood_skill_data(data)

    return data_to_table


def read_blood_skill_data(data: Dict[int, Dict[int, Dict[Union[int, str], Dict]]], player_talent: List[str]):
    """
    根据技能统计数据猜测流血时间轴
    :param data:
    :return:
    """
    # 炼狱技能战斗中无法替换，不会冲突
    LiuXue_GeLie = {29187: 0, 29188: 0, 29186: 1, 29185: 1}    # 子技能id所对应的是否有割裂buff
    GeLie = {13308: 1, 20989: 1}    # 闪刀子技能

    # 斩闪流血的全部时间数据
    blood_data = []


    skill_lx = data.get(8249)
    if not skill_lx:
        return

    for lv in range(28, 0, -1):
        lx_data = skill_lx.get(lv)
        if not lx_data:
            continue
        else:
            lx_data.pop('szName')

            # 直接将取出的流血技能合并至总技能
            for i in lx_data:
                blood_data.append((i, 8249))
            break
    else:
        return

    # print(lx_data)
    # 到这里是取出了流血，且流血只需要释放时间

    # zd_data = {}
    for zhandao_id in LiuXue_GeLie:
        _skill_zd = data.get(zhandao_id)
        if not _skill_zd:
            continue
        else:
            for lv in range(28, 0, -1):
                _zd_data = _skill_zd.get(lv)
                if not _zd_data:
                    continue
                else:
                    _zd_data.pop('szName')

                    # 直接将取出的斩刀技能合并至总技能
                    # zd_data.update({i: zhandao_id for i in _zd_data})
                    for i in _zd_data:
                        blood_data.append((i, zhandao_id))
                    break
    # if not zd_data:
    #     return

    # print(zd_data)
    # 到这里是取出了斩刀时间及斩刀对应的id

    # sd_data = []
    for shandao_id in GeLie:
        _skill_sd = data.get(shandao_id)
        if not _skill_sd:
            continue
        else:
            for lv in range(28, 0, -1):
                _sd_data = _skill_sd.get(lv)
                if not _sd_data:
                    continue
                else:
                    _sd_data.pop('szName')

                    # 直接将取出的闪刀技能合并至总技能
                    # sd_data += [i for i in _sd_data]
                    for i in _sd_data:
                        blood_data.append((i, shandao_id))
                    break
    # if sd_data:
    #     sd_data.sort()

    # if not sd_data:
    #     return
    # 循环允许不打闪刀

    # print(sd_data)
    # 取出闪刀所对应时间，闪刀序列允许为空

    blood_data.sort(key=lambda i: i[0])

    ret = set()
    # 状态
    start_blood_time = 0
    latest_blood_time = 0
    has_gelie = 0

    # 是否点出了割裂
    # GELIE = 1 if '割裂' in player_talent else 0
    # 流血间隔时间
    LIANYU = 1000 if '炼狱' in player_talent else 2000

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
                        ret.add((start_blood_time, latest_blood_time))
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
                            ret.add((start_blood_time, latest_blood_time))
                            start_blood_time = time

    # 全部结束的情况
    if not start_blood_time == 0:
        ret.add((start_blood_time, latest_blood_time))

    pass




















