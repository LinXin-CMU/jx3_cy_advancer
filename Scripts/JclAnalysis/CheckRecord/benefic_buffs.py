# coding: utf-8
# author: LinXin
# 增益buff
benefic_buffs = {
    "江湖": {
        3220: {'Name': '共战江湖', 'Level': 10, 'attrs': {'atAllDamageAddPercent': 51, 'atFinalMaxLifeAddPercent': 51}}
    },
    "天策": {
        362: {'Name': '撼如雷', 'Level': 8, 'attrs': {'atFinalMaxLifeAddPercent': 51, 'atPhysicsAttackPowerPercent': 51}},
        661: {'Name': '破风', 'Level': 30, 'attrs': {'atPhysicsShieldBase': -810}},
        936: {'Name': '卫公折冲五阵', 'Level': 1, 'attrs': {'atPhysicsAttackPowerPercent': 51}},
        6363: {'Name': '激雷', 'Level': 1, 'attrs': {'atPhysicsOvercomePercent': 205, 'atPhysicsAttackPowerPercent': 205}},
        12717: {'Name': '破风增强', 'Level': 30, 'attrs': {'atPhysicsShieldBase': -1080}},
        23107: {'Name': '号令三军', 'Level': 1, 'attrs': {'atStrainBase': 240}}
    },
    "万花": {
        112: {'Name': '清心静气', 'Level': 8, 'attrs': {'atMaxLifePercentAdd': 52}},
        23305: {'Name': '秋肃', 'Level': 1, 'attrs': {'atPhysicsDamageCoefficient': 51, 'atSolarDamageCoefficient': 51, 'atNeutralDamageCoefficient': 51, 'atLunarDamageCoefficient': 51, 'atPoisonDamageCoefficient': 51}}
    },
    "纯阳": {
        378: {'Name': '碎星辰', 'Level': 7, 'attrs': {'atPhysicsCriticalDamagePowerPercent': 102}},
        950: {'Name': '北斗七星五阵', 'Level': 1, 'attrs': {'atPhysicsCriticalStrikePercent': 10}}
    },
    "七秀": {
        673: {'Name': '袖气', 'Level': 10, 'attrs': {'atBasePotentialAdd': 111, 'atMagicShield': 154}},
        20938: {'Name': '左旋右转', 'Level': 1, 'attrs': {'atSurplusValueBase': 500}},
        23573: {'Name': '泠风解怀', 'Level': 1, 'attrs': {'atAllDamageAddPercent': 100}}
    },
    "少林": {
        382: {'Name': '般若诀', 'Level': 10, 'attrs': {'atPhysicsShieldBase': 145, 'atMagicShield': 130}},
        10208: {'Name': '弘法', 'Level': 1, 'attrs': {'atStrainBase': 240}}
    },
    "藏剑": {
        1739: {'Name': '梅隐香', 'Level': 6, 'attrs': {'atPhysicsCriticalDamagePowerPercent': 51}},
        21236: {'Name': '剑锋百锻', 'Level': 5, 'attrs': {'atMeleeWeaponDamagePercent': 717}}
    },
    "丐帮": {
        6345: {'Name': '降龙伏虎五阵', 'Level': 1, 'attrs': {'atPhysicsOvercomeBase': 350}},
        7180: {'Name': '酣畅淋漓', 'Level': 1, 'attrs': {'atPhysicsCriticalStrikePercent': 102}}
    },
    "明教": {
        4058: {'Name': '戒火', 'Level': 1, 'attrs': {'atPhysicsDamageCoefficient': 21, 'atSolarDamageCoefficient': 21, 'atNeutralDamageCoefficient': 21, 'atLunarDamageCoefficient': 21, 'atPoisonDamageCoefficient': 21}},
        4246: {'Name': '朝圣言', 'Level': 1, 'attrs': {'atStrainBase': 240}},
        4418: {'Name': '烈日', 'Level': 1, 'attrs': {'atSolarDamageCoefficient': 51, 'atLunarDamageCoefficient': 51}},
        9744: {'Name': '朝圣言', 'Level': 1, 'attrs': {'atStrainBase': 360}}
    },
    "五毒": {
        12334: {'Name': '圣蝎附体', 'Level': 1, 'attrs': {'atAccelerateCDTimer': 61}}
    },
    "唐门": {
        3308: {'Name': '流星赶月五阵', 'Level': 1, 'attrs': {'atPhysicsCriticalStrikePercent': 51}},
        3310: {'Name': '千机百变五阵', 'Level': 1, 'attrs': {'atPhysicsCriticalStrikePercent': 51}}
    },
    "苍云": {
        8248: {'Name': '虚弱', 'Level': 1, 'attrs': {'atPhysicsShieldPercent': -51}},
        8403: {'Name': '锋凌横绝五阵', 'Level': 1, 'attrs': {'atPhysicsCriticalDamagePowerPercent': 21}},
        8504: {'Name': '振奋', 'Level': 1, 'attrs': {'atPhysicsOvercomeBase': 25, 'atMagicOvercome': 25}},
        10031: {'Name': '寒啸千军', 'Level': 1, 'attrs': {'atPhysicsOvercomePercent': 204, 'atLunarOvercomePercent': 204, 'atNeutralOvercomePercent': 204, 'atPoisonOvercomePercent': 204, 'atSolarOvercomePercent': 204}}
    },
    "长歌": {
        23543: {'Name': '梅花三弄', 'Level': 1, 'attrs': {'atAllShieldIgnorePercent': 154}}
    },
    "霸刀": {
        11158: {'Name': '霜岚洗锋五阵', 'Level': 1, 'attrs': {'atPhysicsCriticalStrikePercent': 51, 'atSolarCriticalStrikePercent': 51, 'atPoisonCriticalStrikePercent': 51, 'atNeutralCriticalStrikePercent': 51, 'atLunarCriticalStrikePercent': 51}},
        11456: {'Name': '疏狂', 'Level': 1, 'attrs': {'atPhysicsAttackPowerPercent': 307, 'atSolarAttackPowerPercent': 307, 'atLunarAttackPowerPercent': 307, 'atNeutralAttackPowerPercent': 307, 'atPoisonAttackPowerPercent': 307}},
    },
    "蓬莱": {

    },
    "凌雪": {
        15961: {'Name': '龙皇雪风五阵', 'Level': 1, 'attrs': {'atPhysicsAttackPowerPercent': 102}}
    },
    "衍天": {
        17596: {'Name': '祝由·水坎', 'Level': 1, 'attrs': {}},
        18337: {'Name': '九星游年五阵', 'Level': 1, 'attrs': {'atAllDamageAddPercent': 154}}
    },
    "药宗": {
        20841: {'Name': '香稠', 'Level': 1, 'attrs': {'atVitalityBasePercentAdd': 205}},
        20854: {'Name': '飘黄', 'Level': 1, 'attrs': {}},
        20877: {'Name': '配伍', 'Level': 1, 'attrs': {'atAgilityBasePercentAdd': 10, 'atStrengthBasePercentAdd': 10, 'atSpiritBasePercentAdd': 10, 'atSpunkBasePercentAdd': 10}}
    }

}