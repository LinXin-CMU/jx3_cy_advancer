# coding: utf-8
# author: LinXin
# 增益buff
BENEFIT_BUFFS = {
    "江湖": {
        "3220_10": {'szName': '共战江湖', 'nLevel': 10, 'szType': 'player', 'tOriginType': 'global', 'attrs': {'atAllDamageAddPercent': 51, 'atFinalMaxLifeAddPercent': 51}},
        "7762_1": {'szName': '义薄云天战', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMagicAttackPowerPercent': 21, 'atPhysicsAttackPowerPercent': 21, 'atTherapyPowerPercent': 21}},
        "15303_1": {'szName': '潮生', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 338, 'atMagicAttackPowerBase': 406}},
        "15303_2": {'szName': '潮生', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 439, 'atMagicAttackPowerBase': 528}},
    },
    "天策": {
        # 玩家技能
        "362_8": {'szName': '撼如雷', 'nLevel': 8, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atFinalMaxLifeAddPercent': 51, 'atPhysicsAttackPowerPercent': 51}},
        "661_30": {'szName': '破风', 'nLevel': 30, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldBase': -810}},
        "936_1": {'szName': '卫公折冲五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsAttackPowerPercent': 51}},
        "6363_1": {'szName': '激雷', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomePercent': 205, 'atPhysicsAttackPowerPercent': 205}},
        "12717_30": {'szName': '破风增强', 'nLevel': 30, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldBase': -1080}},
        "23107_1": {'szName': '号令三军', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 240}},
        # 特殊武器
        "16466_1": {'szName': '赤雷裂空', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 30}},
        "16871_1": {'szName': '化干戈', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atLunarOvercomeBase': 77, 'atSolarOvercomeBase': 77, 'atPoisonOvercomeBase': 77, 'atNeutralOvercomeBase': 77, 'atPhysicsOvercomeBase': 77}},
        "16871_2": {'szName': '化干戈', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atLunarOvercomeBase': 179, 'atSolarOvercomeBase': 179, 'atPoisonOvercomeBase': 179, 'atNeutralOvercomeBase': 179, 'atPhysicsOvercomeBase': 179}},
    },
    "万花": {
        # 玩家技能
        "112_8": {'szName': '清心静气', 'nLevel': 8, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMaxLifePercentAdd': 52}},
        "9724_7": {'szName': '毫针', 'nLevel': 7, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldBase': 3350}},
        "23305_1": {'szName': '秋肃', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 51, 'atSolarDamageCoefficient': 51, 'atNeutralDamageCoefficient': 51, 'atLunarDamageCoefficient': 51, 'atPoisonDamageCoefficient': 51}},
        # 特殊武器
    },
    "纯阳": {
        # 玩家技能
        "378_7": {'szName': '碎星辰', 'nLevel': 7, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalDamagePowerPercent': 102}},
        "950_1": {'szName': '北斗七星五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalStrikeBaseRate': 10}},
        "13846_2": {'szName': '行天道', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalDamagePowerPercent': 102, 'atPhysicsCriticalStrikeBaseRate': 51}},
        # 特殊武器
        "16680_1": {'szName': '画影残月', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 31}}
    },
    "七秀": {
        # 玩家技能
        "673_10": {'szName': '袖气', 'nLevel': 10, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atBasePotentialAdd': 111, 'atMagicShield': 154}},
        "20938_1": {'szName': '左旋右转', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atSurplusValueBase': 500}},
        "23573_1": {'szName': '泠风解怀', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllDamageAddPercent': 100}},
        # 特殊武器
        "3098_1": {'szName': '曼舞', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 2}},
        "3098_2": {'szName': '曼舞', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 17}},
        "16330_1": {'szName': '穿林', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 20, 'atLunarDamageCoefficient': 20, 'atNeutralDamageCoefficient': 20, 'atPoisonDamageCoefficient': 20, 'atSolarDamageCoefficient': 20}},
        "16330_2": {'szName': '穿林', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 31, 'atLunarDamageCoefficient': 31, 'atNeutralDamageCoefficient': 31, 'atPoisonDamageCoefficient': 31, 'atSolarDamageCoefficient': 31}},
        "16330_3": {'szName': '穿林', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 31, 'atLunarDamageCoefficient': 31, 'atNeutralDamageCoefficient': 31, 'atPoisonDamageCoefficient': 31, 'atSolarDamageCoefficient': 31}},
        "16330_4": {'szName': '穿林', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 31, 'atLunarDamageCoefficient': 31, 'atNeutralDamageCoefficient': 31, 'atPoisonDamageCoefficient': 31, 'atSolarDamageCoefficient': 31}},
        "16331_1": {'szName': '红蝶', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 40}},
        "16331_2": {'szName': '红蝶', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 40}},
        "16331_3": {'szName': '红蝶', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 40}},
        "16331_4": {'szName': '红蝶', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 40}},
        "16365_1": {'szName': '镜中寒樱', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 5, 'atPhysicsDamageCoefficient': 5}},
        "16365_2": {'szName': '镜中寒樱', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 10, 'atPhysicsDamageCoefficient': 10}},
        "16365_3": {'szName': '镜中寒樱', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 15, 'atPhysicsDamageCoefficient': 15}},
        "16365_4": {'szName': '镜中寒樱', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 20, 'atPhysicsDamageCoefficient': 20}},
        "16365_5": {'szName': '镜中寒樱', 'nLevel': 5, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 25, 'atPhysicsDamageCoefficient': 25}},
        "16365_6": {'szName': '镜中寒樱', 'nLevel': 6, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 30, 'atPhysicsDamageCoefficient': 30}},
        "16365_7": {'szName': '镜中寒樱', 'nLevel': 7, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 35, 'atPhysicsDamageCoefficient': 35}},
        "16365_8": {'szName': '镜中寒樱', 'nLevel': 8, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 41, 'atPhysicsDamageCoefficient': 41}},
        "16365_9": {'szName': '镜中寒樱', 'nLevel': 9, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 46, 'atPhysicsDamageCoefficient': 46}},
        "16365_10": {'szName': '镜中寒樱', 'nLevel': 10, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_11": {'szName': '镜中寒樱', 'nLevel': 11, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_12": {'szName': '镜中寒樱', 'nLevel': 12, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_13": {'szName': '镜中寒樱', 'nLevel': 13, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_14": {'szName': '镜中寒樱', 'nLevel': 14, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_15": {'szName': '镜中寒樱', 'nLevel': 15, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_16": {'szName': '镜中寒樱', 'nLevel': 16, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_17": {'szName': '镜中寒樱', 'nLevel': 17, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_18": {'szName': '镜中寒樱', 'nLevel': 18, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_19": {'szName': '镜中寒樱', 'nLevel': 19, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16365_20": {'szName': '镜中寒樱', 'nLevel': 20, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atLunarDamageCoefficient': 51, 'atPhysicsDamageCoefficient': 51}},
        "16369_1": {'szName': '傲雪暗香', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 10, 'atNeutralAttackPowerBase': 10, 'atLunarAttackPowerPercent': 10, 'atPoisonAttackPowerPercent': 10, 'atSolarAttackPowerPercent': 10}},
        "16369_2": {'szName': '傲雪暗香', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 20, 'atNeutralAttackPowerBase': 20, 'atLunarAttackPowerPercent': 20, 'atPoisonAttackPowerPercent': 20, 'atSolarAttackPowerPercent': 20}},
        "16369_3": {'szName': '傲雪暗香', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 30, 'atNeutralAttackPowerBase': 30, 'atLunarAttackPowerPercent': 30, 'atPoisonAttackPowerPercent': 30, 'atSolarAttackPowerPercent': 30}},
        "16369_4": {'szName': '傲雪暗香', 'nLevel': 4, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 30, 'atNeutralAttackPowerBase': 30, 'atLunarAttackPowerPercent': 30, 'atPoisonAttackPowerPercent': 30, 'atSolarAttackPowerPercent': 30}},
        "16369_5": {'szName': '傲雪暗香', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 30, 'atNeutralAttackPowerBase': 30, 'atLunarAttackPowerPercent': 30, 'atPoisonAttackPowerPercent': 30, 'atSolarAttackPowerPercent': 30}},
        "16369_6": {'szName': '傲雪暗香', 'nLevel': 6, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 30, 'atNeutralAttackPowerBase': 30, 'atLunarAttackPowerPercent': 30, 'atPoisonAttackPowerPercent': 30, 'atSolarAttackPowerPercent': 30}},

    },
    "少林": {
        # 玩家技能
        "382_10": {'szName': '般若诀', 'nLevel': 10, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldBase': 145, 'atMagicShield': 130}},
        "10208_1": {'szName': '弘法', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 240}}
        # 特殊武器
    },
    "藏剑": {
        # 玩家技能
        "1739_6": {'szName': '梅隐香', 'nLevel': 6, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalDamagePowerPercent': 51}},
        "21236_5": {'szName': '剑锋百锻', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMeleeWeaponDamagePercent': 717}}
        # 特殊武器
    },
    "丐帮": {
        # 玩家技能
        "6345_1": {'szName': '降龙伏虎五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsOvercomeBase': 350}},
        "7180_1": {'szName': '酣畅淋漓', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalStrikeBaseRate': 102}}
        # 特殊武器
    },
    "明教": {
        # 玩家技能
        "4058_1": {'szName': '戒火', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21, 'atSolarDamageCoefficient': 21, 'atNeutralDamageCoefficient': 21, 'atLunarDamageCoefficient': 21, 'atPoisonDamageCoefficient': 21}},
        "4246_1": {'szName': '朝圣言', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 240}},
        "4418_1": {'szName': '烈日', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 51, 'atLunarDamageCoefficient': 51}},
        "9744_1": {'szName': '朝圣言', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 360}},
        # 特殊武器
        "15850_1": {'szName': '琉璃灼烧', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 4}},
        "15850_2": {'szName': '琉璃灼烧', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 4}},
    },
    "五毒": {
        # 玩家技能
        "12334_1": {'szName': '圣蝎附体', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAccelerateCDTimer': 61}}
        # 特殊武器
    },
    "唐门": {
        # 玩家技能
        "3308_1": {'szName': '流星赶月五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalStrikeBaseRate': 51}},
        "3310_1": {'szName': '千机百变五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalStrikeBaseRate': 51}}
        # 特殊武器
    },
    "苍云": {
        "8248_1": {'szName': '虚弱', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldPercent': -51}},
        "8504_1": {'szName': '振奋', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 25, 'atMagicOvercome': 25}},
        "10031_1": {'szName': '寒啸千军', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomePercent': 204, 'atLunarOvercomePercent': 204, 'atNeutralOvercomePercent': 204, 'atPoisonOvercomePercent': 204, 'atSolarOvercomePercent': 204}}
    },
    "长歌": {
        # 玩家技能
        "9334_2": {'szName': '梅花三弄', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllShieldIgnorePercent': 154}},
        "9334_4": {'szName': '绕梁', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllShieldIgnorePercent': 154}},
        # 特殊武器
        "10530_1": {'szName': '破甲', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        "10530_2": {'szName': '破甲', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        "10530_3": {'szName': '破甲', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        "10530_4": {'szName': '破甲', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        "10530_5": {'szName': '破甲', 'nLevel': 5, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        "10530_6": {'szName': '破甲', 'nLevel': 6, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsDamageCoefficient': 21}},
        "10533_1": {'szName': '入世', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 42}},
        "10533_2": {'szName': '入世', 'nLevel': 2, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 63}},
        "10533_3": {'szName': '入世', 'nLevel': 3, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 41}},
        "10533_4": {'szName': '入世', 'nLevel': 4, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 38}},
        "10533_5": {'szName': '入世', 'nLevel': 5, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 126}},
        "10533_6": {'szName': '入世', 'nLevel': 6, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atSolarDamageCoefficient': 52}},
        "11377_1": {'szName': '悲歌', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 41}},
        "11377_2": {'szName': '悲歌', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase': 20}},
        "16911_1": {'szName': '弄梅', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllShieldIgnorePercent': 205, 'atPhysicsOvercomeBase': 700, 'atNeutralOvercomeBase': 700, 'atPoisonOvercomeBase': 700, 'atSolarOvercomeBase': 700, 'atLunarOvercomeBase': 700}},
        "16936_1": {'szName': '烈雷', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 700, 'atMagicAttackPowerBase': 700}},
        "16937_1": {'szName': '风雷引', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}}
    },
    "霸刀": {
        # 玩家技能
        "11158_1": {'szName': '霜岚洗锋五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalStrikeBaseRate': 51, 'atSolarCriticalStrikeBaseRate': 51, 'atPoisonCriticalStrikeBaseRate': 51, 'atNeutralCriticalStrikeBaseRate': 51, 'atLunarCriticalStrikeBaseRate': 51}},
        "11456_1": {'szName': '疏狂', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 307, 'atSolarAttackPowerPercent': 307, 'atLunarAttackPowerPercent': 307, 'atNeutralAttackPowerPercent': 307, 'atPoisonAttackPowerPercent': 307}},
        # 特殊武器
    },
    "蓬莱": {
        # 玩家技能
        # 特殊武器
    },
    "凌雪": {
        # 玩家技能
        "15961_1": {'szName': '龙皇雪风五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsAttackPowerPercent': 102}}
        # 特殊武器
    },
    "衍天": {
        # 玩家技能
        "17596_1": {'szName': '祝由·水坎', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}},
        "18337_1": {'szName': '九星游年五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atAllDamageAddPercent': 154}}
        # 特殊武器
    },
    "药宗": {
        # 玩家技能
        "20841_1": {'szName': '香稠', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atVitalityBasePercentAdd': 205}},
        "20854_1": {'szName': '飘黄', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}},
        "20877_1": {'szName': '配伍', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAgilityBasePercentAdd': 10, 'atStrengthBasePercentAdd': 10, 'atSpiritBasePercentAdd': 10, 'atSpunkBasePercentAdd': 10}}
        # 特殊武器
    }

}


SELF_BUFFS = {
    # 玩家技能
    "8244_5": {'szName': '血怒', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 102}},
    "8248_1": {'szName': '虚弱', 'nLevel': 1, 'szType': 'npc', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldPercent': -51}},
    "8249_22": {'szName': '流血', 'nLevel': 22, 'szType': 'target', 'tOriginType': 'buff', 'attrs': {}},
    "8267_1": {'szName': '恋战', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalStrikeBaseRate': 30}},
    "8271_1": {'szName': '寒甲', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 300}},
    "8272_1": {'szName': '坚铁', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryBaseRate': 61}},
    "8385_1": {'szName': '血怒', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 133}},
    "8386_1": {'szName': '血怒', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsShieldPercent': 133, 'atLunarMagicShieldPercent': 133, 'atNeutralMagicShieldPercent': 133, 'atPoisonMagicShieldPercent': 133, 'atSolarMagicShieldPercent': 133}},
    "8403_1": {'szName': '锋凌横绝五阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsCriticalDamagePowerPercent': 21}},
    "8404_1": {'szName': '锋凌横绝六阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsAttackPowerPercent': 102}},
    "8484_1": {'szName': '锋凌横绝四阵', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'core', 'attrs': {'atPhysicsOvercomePercent': 153}},
    "8423_1": {'szName': '从容', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 205}},
    "8448_1": {'szName': '盾挡', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 205, 'atParryValuePercent': 102}},
    "8448_2": {'szName': '盾挡', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 410, 'atParryValuePercent': 204}},
    "8448_3": {'szName': '盾挡', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 614, 'atParryValuePercent': 306}},
    "8448_4": {'szName': '盾挡', 'nLevel': 4, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 819, 'atParryValuePercent': 409}},
    "8448_5": {'szName': '盾挡', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1024, 'atParryValuePercent': 512}},
    "8448_6": {'szName': '盾挡', 'nLevel': 6, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1228, 'atParryValuePercent': 614}},
    "8448_7": {'szName': '盾挡', 'nLevel': 7, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1433, 'atParryValuePercent': 716}},
    "8448_8": {'szName': '盾挡', 'nLevel': 8, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1638, 'atParryValuePercent': 819}},
    "8448_9": {'szName': '盾挡', 'nLevel': 9, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1843, 'atParryValuePercent': 921}},
    "8448_10": {'szName': '盾挡', 'nLevel': 10, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 2048, 'atParryValuePercent': 1024}},
    "8448_11": {'szName': '盾挡', 'nLevel': 11, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 2252, 'atParryValuePercent': 1126}},
    "8499_1": {'szName': '盾挡', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 164, 'atParryValuePercent': 82}},
    "8499_2": {'szName': '盾挡', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 328, 'atParryValuePercent': 164}},
    "8499_3": {'szName': '盾挡', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 492, 'atParryValuePercent': 246}},
    "8499_4": {'szName': '盾挡', 'nLevel': 4, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 655, 'atParryValuePercent': 328}},
    "8499_5": {'szName': '盾挡', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 819, 'atParryValuePercent': 410}},
    "8499_6": {'szName': '盾挡', 'nLevel': 6, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 983, 'atParryValuePercent': 492}},
    "8499_7": {'szName': '盾挡', 'nLevel': 7, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1147, 'atParryValuePercent': 573}},
    "8499_8": {'szName': '盾挡', 'nLevel': 8, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1311, 'atParryValuePercent': 655}},
    "8499_9": {'szName': '盾挡', 'nLevel': 9, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1475, 'atParryValuePercent': 737}},
    "8499_10": {'szName': '盾挡', 'nLevel': 10, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1638, 'atParryValuePercent': 819}},
    "8499_11": {'szName': '盾挡', 'nLevel': 11, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryPercent': 1802, 'atParryValuePercent': 901}},
    "8504_1": {'szName': '振奋', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 25, 'atMagicOvercome': 25}},
    "8627_1": {'szName': '刀魂', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerPercent': 154}},
    "9889_1": {'szName': '蔑视', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllShieldIgnorePercent': 512}},
    "10031_1": {'szName': '寒啸千军', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomePercent': 204, 'atLunarOvercomePercent': 204, 'atNeutralOvercomePercent': 204, 'atPoisonOvercomePercent': 204, 'atSolarOvercomePercent': 204}},
    "14309_1": {'szName': '锋鸣', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomePercent': 154}},
    "14964_1": {'szName': '崇云', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryValuePercent': 154}},
    "17176_1": {'szName': '分野', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllDamageAddPercent': 51}},
    "17772_1": {'szName': '寒甲', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 30000}},
    "17885_5": {'szName': '铁骨', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atVitalityToPhysicsAttackPowerCof': 41, 'atVitalityToPhysicsOverComeCof': 21}},
    "17885_6": {'szName': '铁骨', 'nLevel': 6, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atVitalityToPhysicsAttackPowerCof': 66, 'atVitalityToPhysicsOverComeCof': 31}},
    "18222_4": {'szName': '严阵', 'nLevel': 4, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atSurplusValueAddPercent': 102}},
    "21308_1": {'szName': '割裂', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}},
    # 装备
    "1428_2": {'szName': '军啸', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsCriticalStrikeBaseRate': 41, 'atPhysicsCriticalDamagePowerPercent': 41}},
    "4761_1": {'szName': '水锐刃', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 5}},
    "4761_3": {'szName': '水痛切', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllTypeCriticalStrike': 4, 'atAllTypeCriticalDamagePowerBase': 4}},
    "4761_8": {'szName': '水不屈', 'nLevel': 8, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryBase': 3, 'atParryValueBase': 37}},
    "4761_9": {'szName': '水无双', 'nLevel': 9, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atStrainBase ': 8}},
    "4761_11": {'szName': '水狂攻', 'nLevel': 11, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMeleeWeaponDamageBase': 1}},
    "4761_13": {'szName': '水急速', 'nLevel': 13, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atHasteBase': 8}},
    "4761_16": {'szName': '水斩流', 'nLevel': 16, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 6}},
    "4761_20": {'szName': '水斩流', 'nLevel': 20, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 8}},
    "4761_24": {'szName': '水斩流', 'nLevel': 24, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 16}},
    "4761_28": {'szName': '水斩流', 'nLevel': 28, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 19}},
    "4761_32": {'szName': '水斩流', 'nLevel': 32, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 22}},
    "4761_36": {'szName': '水斩流', 'nLevel': 36, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 25}},
    "4761_40": {'szName': '水斩流', 'nLevel': 40, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 30}},
    "4761_44": {'szName': '水斩流', 'nLevel': 44, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 40}},
    "4761_48": {'szName': '水斩流', 'nLevel': 48, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 44}},
    "4761_52": {'szName': '水斩流', 'nLevel': 52, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 51}},
    "16340_3": {'szName': '水痛切', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllTypeCriticalStrike': 364, 'atAllTypeCriticalDamagePowerBase': 364}},
    "16340_4": {'szName': '水急速', 'nLevel': 4, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atHasteBase': 439}},
    "4767_1": {'szName': '风锐刃', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 106}},
    "4767_4": {'szName': '风痛切', 'nLevel': 4, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllTypeCriticalStrike': 40, 'atAllTypeCriticalDamagePowerBase': 100}},
    "4767_5": {'szName': '风斩铁', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 94}},
    "4767_11": {'szName': '风不屈', 'nLevel': 11, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryBase': 63, 'atParryValueBase': 715}},
    "4767_14": {'szName': '风狂攻', 'nLevel': 14, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMeleeWeaponDamageBase': 34}},
    "6330_1": {'szName': '彩球赤', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMagicAttackPowerBase': 1, 'atPhysicsAttackPowerBase': 1}},
    "6360_1": {'szName': '风锐刃', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 251}},
    "6360_4": {'szName': '风痛切', 'nLevel': 4, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllTypeCriticalStrike': 100, 'atAllTypeCriticalDamagePowerBase': 235}},
    "6360_5": {'szName': '风斩铁', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 384}},
    "6360_11": {'szName': '风不屈', 'nLevel': 11, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atParryBase': 135, 'atParryValueBase': 3913}},
    "6360_14": {'szName': '风狂攻', 'nLevel': 14, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atMeleeWeaponDamageBase': 57}},
    "6360_15": {'szName': '风急速', 'nLevel': 15, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atHasteBase': 160}},
    "6360_18": {'szName': '风斩流', 'nLevel': 18, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 393}},
    "6360_23": {'szName': '风斩流', 'nLevel': 23, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 427}},
    "6360_28": {'szName': '风斩流', 'nLevel': 28, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 1409}},
    "6360_33": {'szName': '风斩流', 'nLevel': 33, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 1491}},
    "6360_38": {'szName': '风斩流', 'nLevel': 38, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 1831}},
    "6360_43": {'szName': '风斩流', 'nLevel': 43, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 1938}},
    "6360_48": {'szName': '风斩流', 'nLevel': 48, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 2113}},
    "6360_53": {'szName': '风斩流', 'nLevel': 53, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 2236}},
    "6360_58": {'szName': '风斩流', 'nLevel': 58, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 2395}},
    "6360_63": {'szName': '风斩流', 'nLevel': 63, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 2534}},
    "6360_68": {'szName': '风斩流', 'nLevel': 68, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 2883}},
    "6360_73": {'szName': '风斩流', 'nLevel': 73, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 3053}},
    "6360_78": {'szName': '风斩流', 'nLevel': 78, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 3845}},
    "6360_83": {'szName': '风斩流', 'nLevel': 83, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 4070}},
    "6360_88": {'szName': '风斩流', 'nLevel': 88, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 4165}},
    "6360_92": {'szName': '风斩流', 'nLevel': 92, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 4410}},
    "6360_95": {'szName': '风斩流', 'nLevel': 95, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 4806}},
    "6360_99": {'szName': '风斩流', 'nLevel': 99, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 5088}},
    "15305_1": {'szName': '溟啸', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 630}},
    "15305_3": {'szName': '溟啸', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 820}},
    "15413_1": {'szName': '御帽', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 125, 'atMagicAttackPowerBase': 150}},
    "15413_2": {'szName': '御帽', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 141, 'atMagicAttackPowerBase': 168}},
    "15413_3": {'szName': '御帽', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 157, 'atMagicAttackPowerBase': 188}},
    "15413_4": {'szName': '御帽', 'nLevel': 4, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 243, 'atMagicAttackPowerBase': 291}},
    "15413_5": {'szName': '御帽', 'nLevel': 5, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 298, 'atMagicAttackPowerBase': 357}},
    "15413_6": {'szName': '御帽', 'nLevel': 6, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 330, 'atMagicAttackPowerBase': 395}},
    "15413_7": {'szName': '御帽', 'nLevel': 7, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 368, 'atMagicAttackPowerBase': 440}},
    "15455_1": {'szName': '伤腰', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllDamageAddPercent': 10}},
    "15455_2": {'szName': '伤腰', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllDamageAddPercent': 51}},
    "16341_1": {'szName': '风斩铁灭气', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsOvercomeBase': 3876, 'atMagicOvercome': 3876}},
    "16956_1": {'szName': '单刀赴会', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}},
    "16956_2": {'szName': '单刀赴会', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}},
    "16956_3": {'szName': '单刀赴会', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {}},
    "16957_1": {'szName': '单刀赴会·战', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 4}},
    "16957_2": {'szName': '单刀赴会·战', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 40}},
    "16957_3": {'szName': '单刀赴会·战', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 100}},
    "16967_1": {'szName': '单刀赴会·溃', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atBeTherapyCoefficient': -5}},
    "18139_1": {'szName': '激奋', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 105, 'atMagicAttackPowerBase': 127}},
    "18139_2": {'szName': '激奋', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 127, 'atMagicAttackPowerBase': 152}},
    "18139_3": {'szName': '激奋', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atPhysicsAttackPowerBase': 148, 'atMagicAttackPowerBase': 177}},
    "18143_1": {'szName': '克制', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atSurplusValueBase': 373}},
    "18143_2": {'szName': '克制', 'nLevel': 2, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atSurplusValueBase': 448}},
    "18143_3": {'szName': '克制', 'nLevel': 3, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atSurplusValueBase': 522}},
    "21648_1": {'szName': '玉简·分山劲', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atAllDamageAddPercent': 31}},
    "21651_1": {'szName': '残卷·铁骨衣', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atHasteBasePercentAdd': 10}},
    "23392_1": {'szName': '子规笛·战', 'nLevel': 1, 'szType': 'player', 'tOriginType': 'buff', 'attrs': {'atSurplusValueBase': 1200}},
}

