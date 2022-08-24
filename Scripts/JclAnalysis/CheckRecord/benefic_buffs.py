# coding: utf-8
# author: LinXin
# 增益buff
benefic_buffs = {
    "江湖": {
        3220_10: {'szName': '共战江湖', 'nLevel': 10, 'szType': 'player', 'tOriginType': 'global', 'attrs': {'atAllDamageAddPercent': 51, 'atFinalMaxLifeAddPercent': 51}},
        7762_1: {'szName': '义薄云天·战', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMagicAttackPowerPercent': 21, 'atPhysicsAttackPowerPercent': 21, 'atTherapyPowerPercent': 21}}
    },
    "天策": {
        # 玩家技能
        362_8: {'szName': '撼如雷', 'nLevel': 8, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atFinalMaxLifeAddPercent': 51, 'atPhysicsAttackPowerPercent': 51}},
        661_30: {'szName': '破风', 'nLevel': 30, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldBase': -810}},
        936_1: {'szName': '卫公折冲五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsAttackPowerPercent': 51}},
        6363_1: {'szName': '激雷', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomePercent': 205, 'atPhysicsAttackPowerPercent': 205}},
        12717_30: {'szName': '破风增强', 'nLevel': 30, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldBase': -1080}},
        23107_1: {'szName': '号令三军', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 240}},
        # 特殊武器
        16466_1: {'szName': '赤雷裂空', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 30}},
        16871_1: {'szName': '化干戈', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atLunarOvercomeBase': 77, 'atSolarOvercomeBase': 77, 'atPoisonOvercomeBase': 77, 'atNeutralOvercomeBase': 77, 'atPhysicsOvercomeBase': 77}},
        16871_2: {'szName': '化干戈', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atLunarOvercomeBase': 179, 'atSolarOvercomeBase': 179, 'atPoisonOvercomeBase': 179, 'atNeutralOvercomeBase': 179, 'atPhysicsOvercomeBase': 179}},
    },
    "万花": {
        # 玩家技能
        112_8: {'szName': '清心静气', 'nLevel': 8, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMaxLifePercentAdd': 52}},
        9724_7: {'szName': '毫针', 'nLevel': 7, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldBase': 3350}},
        23305_1: {'szName': '秋肃', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 51, 'atSolarDamageCoefficient': 51, 'atNeutralDamageCoefficient': 51, 'atLunarDamageCoefficient': 51, 'atPoisonDamageCoefficient': 51}},
        # 特殊武器
    },
    "纯阳": {
        # 玩家技能
        378_7: {'szName': '碎星辰', 'nLevel': 7, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalDamagePowerPercent': 102}},
        950_1: {'szName': '北斗七星五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalStrikePercent': 10}},
        13846_2: {'szName': '行天道', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalDamagePowerPercent': 102, 'atPhysicsCriticalStrikePercent': 51}},
        # 特殊武器
        16680_1: {'szName': '画影残月', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 31}}
    },
    "七秀": {
        # 玩家技能
        673_10: {'szName': '袖气', 'nLevel': 10, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atBasePotentialAdd': 111, 'atMagicShield': 154}},
        20938_1: {'szName': '左旋右转', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atSurplusValueBase': 500}},
        23573_1: {'szName': '泠风解怀', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllDamageAddPercent': 100}},
        # 特殊武器
        3098_1: {'szName': '曼舞', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 2}},
        3098_2: {'szName': '曼舞', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 17}},
        16330_1: {'szName': '穿林', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 20, 'atLunarDamageCoefficient': 20, 'atNeutralDamageCoefficient': 20, 'atPoisonDamageCoefficient': 20, 'atSolarDamageCoefficient': 20}},
        16330_2: {'szName': '穿林', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 31, 'atLunarDamageCoefficient': 31, 'atNeutralDamageCoefficient': 31, 'atPoisonDamageCoefficient': 31, 'atSolarDamageCoefficient': 31}},
        16330_3: {'szName': '穿林', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 31, 'atLunarDamageCoefficient': 31, 'atNeutralDamageCoefficient': 31, 'atPoisonDamageCoefficient': 31, 'atSolarDamageCoefficient': 31}},
        16330_4: {'szName': '穿林', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 31, 'atLunarDamageCoefficient': 31, 'atNeutralDamageCoefficient': 31, 'atPoisonDamageCoefficient': 31, 'atSolarDamageCoefficient': 31}},
        16331_1: {'szName': '红蝶', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 40}},
        16331_2: {'szName': '红蝶', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 40}},
        16331_3: {'szName': '红蝶', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 40}},
        16331_4: {'szName': '红蝶', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 40}},
        16365_1: {'szName': '镜中寒樱', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 5, 'atPhysicsDamageCoefficient': 5}},
        16365_2: {'szName': '镜中寒樱', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 10, 'atPhysicsDamageCoefficient': 10}},
        16365_3: {'szName': '镜中寒樱', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 15, 'atPhysicsDamageCoefficient': 15}},
        16365_4: {'szName': '镜中寒樱', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 20, 'atPhysicsDamageCoefficient': 20}},
        16365_5: {'szName': '镜中寒樱', 'nLevel': 5, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 25, 'atPhysicsDamageCoefficient': 25}},
        16365_6: {'szName': '镜中寒樱', 'nLevel': 6, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 30, 'atPhysicsDamageCoefficient': 30}},
        16365_7: {'szName': '镜中寒樱', 'nLevel': 7, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 35, 'atPhysicsDamageCoefficient': 35}},
        16365_8: {'szName': '镜中寒樱', 'nLevel': 8, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 41, 'atPhysicsDamageCoefficient': 41}},
        16365_9: {'szName': '镜中寒樱', 'nLevel': 9, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 46, 'atPhysicsDamageCoefficient': 46}},
        16365_10: {'szName': '镜中寒樱', 'nLevel': 10, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_11: {'szName': '镜中寒樱', 'nLevel': 11, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_12: {'szName': '镜中寒樱', 'nLevel': 12, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_13: {'szName': '镜中寒樱', 'nLevel': 13, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_14: {'szName': '镜中寒樱', 'nLevel': 14, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_15: {'szName': '镜中寒樱', 'nLevel': 15, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_16: {'szName': '镜中寒樱', 'nLevel': 16, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_17: {'szName': '镜中寒樱', 'nLevel': 17, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_18: {'szName': '镜中寒樱', 'nLevel': 18, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_19: {'szName': '镜中寒樱', 'nLevel': 19, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16365_20: {'szName': '镜中寒樱', 'nLevel': 20, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        16369_1: {'szName': '傲雪暗香', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 10, 'atNeutralAttackPowerBase': 10, 'atLunarAttackPowerPercent': 10, 'atPoisonAttackPowerPercent': 10, 'atSolarAttackPowerPercent': 10}},
        16369_2: {'szName': '傲雪暗香', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 20, 'atNeutralAttackPowerBase': 20, 'atLunarAttackPowerPercent': 20, 'atPoisonAttackPowerPercent': 20, 'atSolarAttackPowerPercent': 20}},
        16369_3: {'szName': '傲雪暗香', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 30, 'atNeutralAttackPowerBase': 30, 'atLunarAttackPowerPercent': 30, 'atPoisonAttackPowerPercent': 30, 'atSolarAttackPowerPercent': 30}},
        16369_4: {'szName': '傲雪暗香', 'nLevel': 4, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 30, 'atNeutralAttackPowerBase': 30, 'atLunarAttackPowerPercent': 30, 'atPoisonAttackPowerPercent': 30, 'atSolarAttackPowerPercent': 30}},
        16369_5: {'szName': '傲雪暗香', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 30, 'atNeutralAttackPowerBase': 30, 'atLunarAttackPowerPercent': 30, 'atPoisonAttackPowerPercent': 30, 'atSolarAttackPowerPercent': 30}},
        16369_6: {'szName': '傲雪暗香', 'nLevel': 6, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 30, 'atNeutralAttackPowerBase': 30, 'atLunarAttackPowerPercent': 30, 'atPoisonAttackPowerPercent': 30, 'atSolarAttackPowerPercent': 30}},

    },
    "少林": {
        # 玩家技能
        382_10: {'szName': '般若诀', 'nLevel': 10, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldBase': 145, 'atMagicShield': 130}},
        10208_1: {'szName': '弘法', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 240}}
        # 特殊武器
    },
    "藏剑": {
        # 玩家技能
        1739_6: {'szName': '梅隐香', 'nLevel': 6, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalDamagePowerPercent': 51}},
        21236_5: {'szName': '剑锋百锻', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMeleeWeaponDamagePercent': 717}}
        # 特殊武器
    },
    "丐帮": {
        # 玩家技能
        6345_1: {'szName': '降龙伏虎五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsOvercomeBase': 350}},
        7180_1: {'szName': '酣畅淋漓', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalStrikePercent': 102}}
        # 特殊武器
    },
    "明教": {
        # 玩家技能
        4058_1: {'szName': '戒火', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21, 'atSolarDamageCoefficient': 21, 'atNeutralDamageCoefficient': 21, 'atLunarDamageCoefficient': 21, 'atPoisonDamageCoefficient': 21}},
        4246_1: {'szName': '朝圣言', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 240}},
        4418_1: {'szName': '烈日', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 51, 'atLunarDamageCoefficient': 51}},
        9744_1: {'szName': '朝圣言', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 360}},
        # 特殊武器
        15850_1: {'szName': '琉璃灼烧', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 4}},
        15850_2: {'szName': '琉璃灼烧', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 4}},
    },
    "五毒": {
        # 玩家技能
        12334_1: {'szName': '圣蝎附体', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAccelerateCDTimer': 61}}
        # 特殊武器
    },
    "唐门": {
        # 玩家技能
        3308_1: {'szName': '流星赶月五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalStrikePercent': 51}},
        3310_1: {'szName': '千机百变五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalStrikePercent': 51}}
        # 特殊武器
    },
    "苍云": {
        8248_1: {'szName': '虚弱', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldPercent': -51}},
        8403_1: {'szName': '锋凌横绝五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalDamagePowerPercent': 21}},
        8504_1: {'szName': '振奋', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 25, 'atMagicOvercome': 25}},
        10031_1: {'szName': '寒啸千军', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomePercent': 204, 'atLunarOvercomePercent': 204, 'atNeutralOvercomePercent': 204, 'atPoisonOvercomePercent': 204, 'atSolarOvercomePercent': 204}}
    },
    "长歌": {
        # 玩家技能
        23543_1: {'szName': '梅花三弄', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllShieldIgnorePercent': 154}},
        # 特殊武器
        10530_1: {'szName': '破甲', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        10530_2: {'szName': '破甲', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        10530_3: {'szName': '破甲', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        10530_4: {'szName': '破甲', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        10530_5: {'szName': '破甲', 'nLevel': 5, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        10530_6: {'szName': '破甲', 'nLevel': 6, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        10533_1: {'szName': '入世', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 42}},
        10533_2: {'szName': '入世', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 63}},
        10533_3: {'szName': '入世', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 41}},
        10533_4: {'szName': '入世', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 38}},
        10533_5: {'szName': '入世', 'nLevel': 5, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 126}},
        10533_6: {'szName': '入世', 'nLevel': 6, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 52}},
        11377_1: {'szName': '悲歌', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 41}},
        11377_2: {'szName': '悲歌', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 20}},
        16911_1: {'szName': '弄梅', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllShieldIgnorePercent': 205, 'atPhysicsOvercomeBase': 700, 'atNeutralOvercomeBase': 700, 'atPoisonOvercomeBase': 700, 'atSolarOvercomeBase': 700, 'atLunarOvercomeBase': 700}},
        16936_1: {'szName': '烈雷', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 700, 'atMagicAttackPowerBase': 700}},
        16937_1: {'szName': '风雷引', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}}
    },
    "霸刀": {
        # 玩家技能
        11158_1: {'szName': '霜岚洗锋五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalStrikePercent': 51, 'atSolarCriticalStrikePercent': 51, 'atPoisonCriticalStrikePercent': 51, 'atNeutralCriticalStrikePercent': 51, 'atLunarCriticalStrikePercent': 51}},
        11456_1: {'szName': '疏狂', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 307, 'atSolarAttackPowerPercent': 307, 'atLunarAttackPowerPercent': 307, 'atNeutralAttackPowerPercent': 307, 'atPoisonAttackPowerPercent': 307}},
        # 特殊武器
    },
    "蓬莱": {
        # 玩家技能
        # 特殊武器
    },
    "凌雪": {
        # 玩家技能
        15961_1: {'szName': '龙皇雪风五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsAttackPowerPercent': 102}}
        # 特殊武器
    },
    "衍天": {
        # 玩家技能
        17596_1: {'szName': '祝由·水坎', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}},
        18337_1: {'szName': '九星游年五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atAllDamageAddPercent': 154}}
        # 特殊武器
    },
    "药宗": {
        # 玩家技能
        20841_1: {'szName': '香稠', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atVitalityBasePercentAdd': 205}},
        20854_1: {'szName': '飘黄', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}},
        20877_1: {'szName': '配伍', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAgilityBasePercentAdd': 10, 'atStrengthBasePercentAdd': 10, 'atSpiritBasePercentAdd': 10, 'atSpunkBasePercentAdd': 10}}
        # 特殊武器
    }

}

