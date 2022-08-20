from lupa import LuaRuntime
from functools import reduce

from Scripts.ReadData.Equips.get_other_data import get_buff_or_skill_from_jx3box
from Sources.Jx3_Datas.JclData import forces, mounts, warn_msgs, dmg_types
from Sources.Jx3_Datas.Jx3Buff import buff
from Sources.Jx3_Datas.Jx3Skill import skill


class TypeReader:
    """数据解析器"""

    def __init__(self):
        # 初始化lua解析器
        self._lua = LuaRuntime()
        self._buff = buff
        self._skill = skill

    def _get_buff(self, *, bf_id=None, level=None) -> dict:
        """
        从Jx3Datas.Jx3Buff中查询目标buff
        :return: dict
        """
        try:
            ret = self._buff[bf_id]
            # 从数据库中读取到对应id
            if level is not None and level in ret:
                ret = ret[level]
            else:
                ret = ret[list(ret.keys())[0]]
            # 查询对应数据
            if ret["Name"] is None:
                # 检查Name字段是否为None
                if ret["BuffName"] is not None:
                    ret["Name"] = ret["BuffName"]
                else:
                    ret["Name"] = bf_id

            return ret
        except KeyError:
            print(f"not found buff: id={bf_id}")
            value = get_buff_or_skill_from_jx3box('buff', bf_id, level)
            return value



    def _get_skill(self, *, sk_id=None, level=None) -> dict:
        """
        从Jx3Datas.Jx3Skill中查询目标skill
        :return: dict
        """
        try:
            ret = self._skill[sk_id]
            # 从数据库中读取到对应id
            if level is not None and level in ret:
                ret = ret[level]
            else:
                ret = ret[list(ret.keys())[0]]
            # 查询对应数据
            if ret["Name"] is None:
                # 检查Name字段是否为None
                if ret["SkillName"] is not None:
                    ret["Name"] = ret["SkillName"]
                else:
                    ret["Name"] = sk_id

            return ret
        except KeyError:
            print(f"not found skill: id={sk_id}")
            value = get_buff_or_skill_from_jx3box('skill', sk_id, level)
            return value


    def read_type(self, data) -> dict:
        """
        将luadata[5]转化为可阅读的记录
        :param data: 一行jcl记录
        :return dict: jcl[5]的分析结果
        """
        # 提取目标内容
        data_type = int(data[4])
        data_lua = self._lua.eval(reduce(lambda i, j: i+j, data[5:]))


        # 分类解析
        match data_type:
            case 1:
                return {
                    'bFighting': data_lua[1],
                    'szUUID': data_lua[2].split('::'),
                    'nDuring': data_lua[3]
                }
            case 2:
                return {
                    'dwID': data_lua[1]
                }
            case 3:
                return {
                    'dwID': data_lua[1]
                }
            case 4:
                try:
                    return {
                        'dwID': data_lua[1],
                        'szName': data_lua[2],
                        'dwForceID': forces[data_lua[3]],
                        'dwMountKungfuID': mounts[data_lua[4]],
                        'nEquipScore': data_lua[5],
                        'aEquip': data_lua[6],
                        'aTalent': self._get_talent(data_lua[7]),
                        'szGUID': data_lua[8]
                    }
                except KeyError:
                    return {
                        'dwID': data_lua[1],
                        'szName': data_lua[2],
                        'dwForceID': data_lua[3],
                        'dwMountKungfuID': data_lua[4],
                        'nEquipScore': data_lua[5],
                        'aEquip': data_lua[6],
                        'aTalent': self._get_talent(data_lua[7]),
                        'szGUID': data_lua[8]
                    }
            case 5:
                return {
                    'dwID': data_lua[1],
                    'bFight': "进入战斗" if data_lua[2] else "离开战斗",
                    'fCurrentLife': data_lua[3],
                    'fMaxLife': data_lua[4],
                    'nCurrentMana': data_lua[5],
                    'nMaxMana': data_lua[6]
                }
            case 6:
                return {
                    'dwID': data_lua[1]
                }
            case 7:
                return {
                    'dwID': data_lua[1]
                }
            case 8:
                return {
                    'dwID': data_lua[1],
                    'szName': data_lua[2],
                    'dwTemplateID': data_lua[3],
                    'dwEmployer': data_lua[4],
                    'nX': data_lua[5],
                    'nY': data_lua[6],
                    'nZ': data_lua[7]
                }
            case 9:
                return {
                    'dwID': data_lua[1],
                    'bFight': "进入战斗" if data_lua[2] else "离开战斗",
                    'fCurrentLife': data_lua[3],
                    'fMaxLife': data_lua[4],
                    'nCurrentMana': data_lua[5],
                    'nMaxMana': data_lua[6]
                }
            case 10:
                return {
                    'dwID': data_lua[1]
                }
            case 11:
                return {
                    'dwID': data_lua[1]
                }
            case 12:
                return {
                    'dwID': data_lua[1],
                    'dwTemplateID': data_lua[2],
                    'nX': data_lua[3],
                    'nY': data_lua[4],
                    'nZ': data_lua[5]
                }
            case 13:
                return {
                    'dwPlayerID': data_lua[1],
                    'bDelete': data_lua[2],
                    'nIndex': data_lua[3],
                    'bCanCancel': 'buff' if data_lua[4] else 'debuff',
                    'dwBuffID': data_lua[5],
                    'szName': self._get_buff(bf_id=data_lua[5], level=data_lua[9])['Name'],
                    'nStackNum': data_lua[6],
                    'nEndFrame': data_lua[7],
                    'bInit': data_lua[8],
                    'nLevel': data_lua[9],
                    'dwSkillSrcID': data_lua[10],
                    'bIsValid': data_lua[11],
                }
            case 14:
                return {
                    'szText': data_lua[1],
                    'dwTalkerID': data_lua[2],
                    'nChannel': data_lua[3],
                    'szName': data_lua[4]
                }
            case 15:
                return {
                    'szWarningType': warn_msgs[data_lua[1]],
                    'szText': data_lua[2]
                }
            case 16:
                return {
                    'dwTeamID': data_lua[1],
                    'dwMemberID': data_lua[2],
                    'nGroupIndex': data_lua[3]
                }
            case 17:
                return {
                    'dwTeamID': data_lua[1],
                    'dwMemberID': data_lua[2],
                    'nOnlineFlag': data_lua[3]
                }
            case 18:
                return {
                    'szText': data_lua[1],
                    'szChannel': data_lua[2]
                }
            case 19:
                return {
                    'dwCaster': data_lua[1],
                    'dwSkillID': data_lua[2],
                    'dwLevel': data_lua[3],
                    'szName': self._get_skill(sk_id=data_lua[2], level=data_lua[3])['Name']
                }
            case 20:
                return {
                    'dwCaster': data_lua[1],
                    'dwSkillID': data_lua[2],
                    'dwLevel': data_lua[3],
                    'nRespond': data_lua[4],
                    'szName': self._get_skill(sk_id=data_lua[2], level=data_lua[3])['Name']
                }
            case 21:
                return {
                    'dwCaster': data_lua[1],
                    'dwTarget': data_lua[2],
                    'bReact': data_lua[3],
                    'nType': 'skill' if int(data_lua[4]) == 1 else 'buff',
                    'dwID': data_lua[5],
                    'dwLevel': data_lua[6],
                    'szName': self._get_item_name(data_lua),
                    'bCriticalStrike': "会心" if data_lua[7] else "未会心",
                    'nCount': data_lua[8],
                    'tResultCount': self._get_damage_type(data_lua)
                }
            case 22:
                return {
                    'dwCaster': data_lua[1],
                    'dwTarget': data_lua[2],
                    'nType': data_lua[3],
                    'dwID': data_lua[4],
                    'dwLevel': data_lua[5],
                    'szName': self._get_event_name(data_lua),
                    'nDamageType': data_lua[6]
                }
            case 23:
                return {
                    'dwCaster': data_lua[1],
                    'dwTarget': data_lua[2],
                    'nType': data_lua[3],
                    'dwID': data_lua[4],
                    'dwLevel': data_lua[5],
                    'szName': self._get_event_name(data_lua),
                }
            case 24:
                return {
                    'dwCaster': data_lua[1],
                    'dwTarget': data_lua[2],
                    'nType': data_lua[3],
                    'dwID': data_lua[4],
                    'dwLevel': data_lua[5],
                    'szName': self._get_event_name(data_lua),
                }
            case 25:
                return {
                    'dwCaster': data_lua[1],
                    'dwTarget': data_lua[2],
                    'nType': data_lua[3],
                    'dwID': data_lua[4],
                    'dwLevel': data_lua[5],
                    'szName': self._get_event_name(data_lua),
                }
            case 26:
                return {
                    'dwCaster': data_lua[1],
                    'dwTarget': data_lua[2],
                    'nType': data_lua[3],
                    'dwID': data_lua[4],
                    'dwLevel': data_lua[5],
                    'szName': self._get_event_name(data_lua),
                }
            case 27:
                return {
                    'dwCharacterID': data_lua[1],
                    'nDeltaLife': data_lua[2]
                }
            case 28:
                return {
                    'dwCharacterID': data_lua[1],
                    'dwKiller': data_lua[2]
                }



    def _get_talent(self, luadata) -> list:
        talent = None
        if luadata is not None:
            for i in range(12):
                qx = luadata[i + 1]
                lv = qx[1]
                sk_id = qx[2]
                if talent is None:
                    talent = [self._get_skill(sk_id=sk_id, level=lv)['Name']]
                else:
                    talent.append(self._get_skill(sk_id=sk_id, level=lv)['Name'])
        return talent

    def _get_item_name(self, luadata) -> str:
        match int(luadata[4]):
            case 1:
                return self._get_skill(sk_id=luadata[5], level=luadata[6])['Name']
            case 2:
                return self._get_buff(bf_id=luadata[5], level=luadata[6])['Name']
            case _:
                print('type error in event=21')

    def _get_event_name(self, luadata) -> str:
        match int(luadata[3]):
            case 1:
                return self._get_skill(sk_id=luadata[4], level=luadata[5])['Name']
            case 2:
                return self._get_buff(bf_id=luadata[4], level=luadata[5])['Name']
            case _:
                print('type error in event 22-26')

    def _get_damage_type(self, luadata) -> dict:
        res_count = None
        for i in range(15):
            if luadata[9][i] is not None:
                dmg_type = dmg_types[i]
                dmg_count = luadata[9][i]
                if res_count is None:
                    res_count = {dmg_type: dmg_count}
                else:
                    res_count[dmg_type] = dmg_count
        if res_count is None:
            res_count = {}
        return res_count
