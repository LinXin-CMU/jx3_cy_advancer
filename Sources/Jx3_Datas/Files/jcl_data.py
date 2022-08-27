log_type = {
    1: 'FIGHT_TIME',  # -- 战斗时间
    2: 'PLAYER_ENTER_SCENE',  # -- 玩家进入场景
    3: 'PLAYER_LEAVE_SCENE',  # -- 玩家离开场景
    4: 'PLAYER_INFO',  # -- 玩家信息数据
    5: 'PLAYER_FIGHT_HINT',  # -- 玩家战斗状态改变
    6: 'NPC_ENTER_SCENE',  # -- NPC进入场景
    7: 'NPC_LEAVE_SCENE',  # -- NPC离开场景
    8: 'NPC_INFO',  # -- NPC信息数据
    9: 'NPC_FIGHT_HINT',  # -- NPC战斗状态改变
    10: 'DOODAD_ENTER_SCENE',  # -- 交互物件进入场景
    11: 'DOODAD_LEAVE_SCENE',  # -- 交互物件离开场景
    12: 'DOODAD_INFO',  # -- 交互物件信息数据
    13: 'BUFF_UPDATE',  # -- BUFF刷新
    14: 'PLAYER_SAY',  # -- 角色喊话（仅记录NPC）
    15: 'ON_WARNING_MESSAGE',  # -- 显示警告框
    16: 'PARTY_ADD_MEMBER',  # -- 团队添加成员
    17: 'PARTY_SET_MEMBER_ONLINE_FLAG',  # -- 团队成员在线状态改变
    18: 'MSG_SYS',  # -- 系统消息
    19: 'SYS_MSG_UI_OME_SKILL_CAST_LOG',  # -- 技能施放日志
    20: 'SYS_MSG_UI_OME_SKILL_CAST_RESPOND_LOG',  # -- 技能施放结果日志
    21: 'SYS_MSG_UI_OME_SKILL_EFFECT_LOG',  # -- 技能最终产生的效果（生命值的变化）
    22: 'SYS_MSG_UI_OME_SKILL_BLOCK_LOG',  # -- 格挡日志
    23: 'SYS_MSG_UI_OME_SKILL_SHIELD_LOG',  # -- 技能被屏蔽日志
    24: 'SYS_MSG_UI_OME_SKILL_MISS_LOG',  # -- 技能未命中目标日志
    25: 'SYS_MSG_UI_OME_SKILL_HIT_LOG',  # -- 技能命中目标日志
    26: 'SYS_MSG_UI_OME_SKILL_DODGE_LOG',  # -- 技能被闪避日志
    27: 'SYS_MSG_UI_OME_COMMON_HEALTH_LOG',  # -- 普通治疗日志
    28: 'SYS_MSG_UI_OME_DEATH_NOTIFY',  # -- 死亡日志
}

type_name = {
    'FIGHT_TIME': '战斗时间',
    'PLAYER_ENTER_SCENE': '玩家进入场景',
    'PLAYER_LEAVE_SCENE': '玩家离开场景',
    'PLAYER_INFO': '玩家信息',
    'PLAYER_FIGHT_HINT': '玩家战斗状态改变',
    'NPC_ENTER_SCENE': 'NPC进入场景',
    'NPC_LEAVE_SCENE': 'NPC离开场景',
    'NPC_INFO': 'NPC信息',
    'NPC_FIGHT_HINT': 'NPC战斗状态改变',
    'DOODAD_ENTER_SCENE': '交互物件进入场景',
    'DOODAD_LEAVE_SCENE': '交互物件离开场景',
    'DOODAD_INFO': '交互物件信息',
    'BUFF_UPDATE': 13,
    'PLAYER_SAY': '喊话',
    'ON_WARNING_MESSAGE': '显示警告框',
    'PARTY_ADD_MEMBER': '团队添加成员',
    'PARTY_SET_MEMBER_ONLINE_FLAG': '团队成员在线状态改变',
    'MSG_SYS': '系统消息',
    'SYS_MSG_UI_OME_SKILL_CAST_LOG': '技能施放',
    'SYS_MSG_UI_OME_SKILL_CAST_RESPOND_LOG': '技能施放结果',
    'SYS_MSG_UI_OME_SKILL_EFFECT_LOG': '血量变化',
    'SYS_MSG_UI_OME_SKILL_BLOCK_LOG': '格挡',
    'SYS_MSG_UI_OME_SKILL_SHIELD_LOG': '免疫',
    'SYS_MSG_UI_OME_SKILL_MISS_LOG': '未命中',
    'SYS_MSG_UI_OME_SKILL_HIT_LOG': '命中',
    'SYS_MSG_UI_OME_SKILL_DODGE_LOG': '闪避',
    'SYS_MSG_UI_OME_COMMON_HEALTH_LOG': '治疗',
    'SYS_MSG_UI_OME_DEATH_NOTIFY': '死亡',
}

forces = {
    0: '江湖',
    3: '天策',
    2: '万花',
    4: '纯阳',
    5: '七秀',
    1: '少林',
    8: '藏剑',
    9: '丐帮',
    10: '明教',
    6: '五毒',
    7: '唐门',
    21: '苍云',
    22: '长歌',
    23: '霸刀',
    24: '蓬莱',
    25: '凌雪',
    211: '衍天',
    212: '药宗',
}

mounts = {
    0: '江湖',
    10003: '易筋经',
    10002: '洗髓经',
    10015: '太虚剑意',
    10014: '紫霞功',
    10021: '花间游',
    10028: '离经易道',
    10026: '傲血战意',
    10062: '铁牢律',
    10081: '冰心诀',
    10080: '云裳心经',
    10175: '毒经',
    10176: '补天诀',
    10224: '惊羽诀',
    10225: '天罗诡道',
    10144: '问水诀',
    10145: '山居剑意',
    10268: '笑尘诀',
    10242: '焚影圣诀',
    10243: '明尊琉璃体',
    10389: '铁骨衣',
    10390: '分山劲',
    10447: '莫问',
    10448: '相知',
    10464: '北傲诀',
    10533: '凌海诀',
    10585: '隐龙诀',
    10615: '太玄经',
    10626: '灵素',
    10627: '无方',
}

warn_msgs = {
    'MSG_NOTICE_GREEN': '提示(绿色)',
    'MSG_NOTICE_YELLOW': '警告(黄色)',
    'MSG_NOTICE_RED': '危险(红色)',
    'MSG_REWARD_GREEN': '提示(绿色)',
    'MSG_REWARD_YELLOW': '警告(黄色)',
    'MSG_REWARD_RED': '危险(红色)',
    'MSG_WARNING_GREEN': '提示(绿色)',
    'MSG_WARNING_YELLOW': '警告(黄色)',
    'MSG_WARNING_RED': '危险(红色)',

}

dmg_types = {
    0: '外功伤害',
    1: '阳性内功伤害',
    2: '混元内功伤害',
    3: '阴性内功伤害',
    4: '毒性内功伤害',
    5: '反弹',
    6: '治疗',
    7: '吸血',
    8: '未知',
    9: '化解',
    10: '未知',
    11: '招架',
    12: '未知',
    13: '有效伤害',
    14: '有效治疗',
}

type_to_event_type = {
    'FIGHT_TIME': 'Time',
    'PLAYER_ENTER_SCENE': 'Player',
    'PLAYER_LEAVE_SCENE': 'Player',
    'PLAYER_INFO': 'Player',
    'PLAYER_FIGHT_HINT': 'Player',
    'NPC_ENTER_SCENE': 'Npc',
    'NPC_LEAVE_SCENE': 'Npc',
    'NPC_INFO': 'Npc',
    'NPC_FIGHT_HINT': 'Npc',
    'DOODAD_ENTER_SCENE': 'Doodad',
    'DOODAD_LEAVE_SCENE': 'Doodad',
    'DOODAD_INFO': 'Doodad',
    'BUFF_UPDATE': 'Buff',
    'PLAYER_SAY': 'Player',
    'ON_WARNING_MESSAGE': 'System',
    'PARTY_ADD_MEMBER': 'Player',
    'PARTY_SET_MEMBER_ONLINE_FLAG': 'Player',
    'MSG_SYS': 'System',
    'SYS_MSG_UI_OME_SKILL_CAST_LOG': 'Skill',
    'SYS_MSG_UI_OME_SKILL_CAST_RESPOND_LOG': 'Skill',
    'SYS_MSG_UI_OME_SKILL_EFFECT_LOG': 'Skill',
    'SYS_MSG_UI_OME_SKILL_BLOCK_LOG': 'Skill',
    'SYS_MSG_UI_OME_SKILL_SHIELD_LOG': 'Skill',
    'SYS_MSG_UI_OME_SKILL_MISS_LOG': 'Skill',
    'SYS_MSG_UI_OME_SKILL_HIT_LOG': 'Skill',
    'SYS_MSG_UI_OME_SKILL_DODGE_LOG': 'Skill',
    'SYS_MSG_UI_OME_COMMON_HEALTH_LOG': 'Player',
    'SYS_MSG_UI_OME_DEATH_NOTIFY': 'Player',
}

slot_to_name_dictionary = {
    'atPhysicsShieldBase': '外防等级'
    , 'atMagicShield': '内防等级'
    , 'atMeleeWeaponDamageBase': '武器伤害'
    , 'atMeleeWeaponDamageRand': '武器伤害浮动'
    , 'atMeleeWeaponAttackSpeedBase': '武器攻击速度'
    , 'atRangeWeaponDamageBase': '暗器伤害'
    , 'atRangeWeaponDamageRand': '暗器伤害'
    , 'atRangeWeaponAttackSpeedBase': '暗器攻击速度'
    , 'atVitalityBase': '体质'
    , 'atAgilityBase': '身法'
    , 'atAgilityBasePercentAdd': '身法'
    , 'atSpunkBase': '元气'
    , 'atSpunkBasePercentAdd': '元气'
    , 'atStrengthBase': '力道'
    , 'atStrengthBasePercentAdd': '力道'
    , 'atSpiritBase': '根骨'
    , 'atSpiritBasePercentAdd': '根骨'
    , 'atVitalityBasePercentAdd': '体质'
    , 'atDecriticalDamagePowerBase': '化劲'
    , 'atDecriticalDamagePowerPercent': '化劲'
    , 'atParryBase': '招架'
    , 'atParryPercent': '招架'
    , 'atParryValueBase': '招架'
    , 'atParryValuePercent': '招架'
    , 'atDodge': '闪避'
    , 'atToughnessBase': '御劲'
    , 'atToughnessPercent': '御劲'
    , 'atGlobalResistPercent': '减伤'
    , 'atDropDefence': '抗摔'
    , 'atHasteBase': '加速'
    , 'atStrainBase': '无双'
    , 'atStrainPercent': '无双'
    , 'atSurplusValueBase': '破招'
    , 'atBasePotentialAdd': '全属性'
    , 'atAllTypeHitValue': '全命中'
    , 'atAllTypeCriticalStrike': '全会心'
    , 'atAddSprintPowerCost': '气力值'
    , 'atAddSprintPowerMax': '气力值'
    , 'atAddSprintPowerRevive': '气力值'
    , 'atActiveThreatCoefficient': '威胁值'
    , 'atLunarAttackPowerBase': '内功攻击'
    , 'atMagicAttackPowerBase': '内功攻击'
    , 'atNeutralAttackPowerBase': '内功攻击'
    , 'atPoisonAttackPowerBase': '内功攻击'
    , 'atSolarAndLunarAttackPowerBase': '内功攻击'
    , 'atSolarAttackPowerBase': '内功攻击'
    , 'atLunarCriticalStrike': '内功会心'
    , 'atLunarCriticalStrikeBaseRate': '内功会心'
    , 'atMagicCriticalStrike': '内功会心'
    , 'atNeutralCriticalStrike': '内功会心'
    , 'atNeutralCriticalStrikeBaseRate': '内功会心'
    , 'atPoisonCriticalStrike': '内功会心'
    , 'atPoisonCriticalStrikeBaseRate': '内功会心'
    , 'atSolarAndLunarCriticalStrike': '内功会心'
    , 'atSolarCriticalStrike': '内功会心'
    , 'atSolarCriticalStrikeBaseRate': '内功会心'
    , 'atLunarHitValue': '内功命中'
    , 'atMagicHitValue': '内功命中'
    , 'atNeutralHitValue': '内功命中'
    , 'atPoisonHitValue': '内功命中'
    , 'atSolarAndLunarHitValue': '内功命中'
    , 'atSolarHitValue': '内功命中'
    , 'atLunarOvercomeBase': '内功破防'
    , 'atMagicOvercome': '内功破防'
    , 'atNeutralOvercomeBase': '内功破防'
    , 'atNeutralOvercomePercent': '内功破防'
    , 'atPoisonOvercomeBase': '内功破防'
    , 'atSolarAndLunarOvercomeBase': '内功破防'
    , 'atSolarOvercomeBase': '内功破防'
    , 'atManaReplenishExt': '内力恢复'
    , 'atManaReplenishPercent': '内力恢复'
    , 'atMaxManaAdditional': '内力上限'
    , 'atMaxManaBase': '内力上限'
    , 'atMaxManaPercentAdd': '内力上限'
    , 'atDamageToManaForSelf': '内力偷取'
    , 'atModifyCostManaPercent': '内力消耗'
    , 'atPhysicsAttackPowerBase': '外功攻击'
    , 'atPhysicsAttackPower': '外功攻击(最终)'
    , 'atPhysicsCriticalStrike': '外功会心'
    , 'atPhysicsHitValue': '外功命中'
    , 'atPhysicsOvercomeBase': '外功破防'
    , 'atLifeReplenishExt': '气血恢复'
    , 'atLifeReplenishPercent': '气血恢复'
    , 'atMaxLifeAdditional': '气血上限'
    , 'atMaxLifeBase': '气血上限'
    , 'atMaxLifePercentAdd': '气血上限'
    , 'atLunarMagicShieldBase': '内功防御'
    , 'atNeutralMagicShieldBase': '内功防御'
    , 'atPoisonMagicShieldBase': '内功防御'
    , 'atSolarMagicShieldBase': '内功防御'
    , 'atPhysicsDefenceAdd': '外功防御'
    , 'atPhysicsShieldAdditional': '外功防御'
    , 'atPhysicsShieldPercent': '外功防御'
    , 'atDamageToLifeForSelf': '生命偷取'
    , 'atDivingFrameBase': '水下呼吸'
    , 'atMoveSpeedPercent': '移动速度'
    , 'atTherapyCoefficient': '治疗成效'
    , 'atTherapyPowerBase': '治疗成效'
    , 'atBeTherapyCoefficient': '被治疗成效'
    , 'atAddHorseSprintPowerCost': '马术气力值'
    , 'atAddHorseSprintPowerMax': '马术气力值'
    , 'atAddHorseSprintPowerRevive': '马术气力值'
    , 'atAllTypeCriticalDamagePowerBase': '全会心效果'
    , 'atLunarCriticalDamagePowerPercent': '内功会心效果'
    , 'atMagicCriticalDamagePowerBase': '内功会心效果'
    , 'atMagicCriticalDamagePowerPercent': '内功会心效果'
    , 'atNeutralCriticalDamagePowerBase': '内功会心效果'
    , 'atNeutralCriticalDamagePowerPercent': '内功会心效果'
    , 'atPoisonCriticalDamagePowerBase': '内功会心效果'
    , 'atPoisonCriticalDamagePowerPercent': '内功会心效果'
    , 'atSolarAndLunarCriticalDamagePowerBase': '内功会心效果'
    , 'atSolarCriticalDamagePowerBase': '内功会心效果'
    , 'atSolarCriticalDamagePowerPercent': '内功会心效果'
    , 'atPhysicsCriticalDamagePowerBase': '外功会心效果'
    , 'atPhysicsCriticalDamagePowerPercent': '外功会心效果'
    , 'atSetEquipmentRecipe': '套装效果秘籍'
}

short_attr_dict = {
    'PhysicsShield': '外防',
    'MagicShield': '内防',
    'Critical': '会心',
    'CriticalDamage': '会效',
    'Overcome': '破防',
    'Strain': '无双',
    'Surplus': '破招',
    'Haste': '加速',
    'Toughness': '御劲',
    'Parry': '招架',
    'Dodge': '闪避'
}

location_dict = {
    'HAT': '帽子',
    'JACKET': '上衣',
    'BELT': '腰带',
    'WRIST': '护腕',
    'BOTTOMS': '下装',
    'SHOES': '鞋子',
    'NECKLACE': '项链',
    'PENDANT': '腰坠',
    'RING_1': '戒指',
    'RING_2': '戒指',
    'SECONDARY_WEAPON': '远程武器',
    'PRIMARY_WEAPON': '近身武器'
}
