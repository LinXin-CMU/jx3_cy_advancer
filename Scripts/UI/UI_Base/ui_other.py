"""
零散函数和变量
"""

from PIL import Image

from CustomClasses.Exceptions import SourceNotFoundError


def set_page(index, func):
    """
    记录当前StackWidget页面序号
    :param index:
    :param func:
    :return:
    """
    self_index = index

    def _inner():
        """
        执行setCurrentIndex的内层
        :return:
        """
        func(self_index)

    return _inner


# 表格列宽
DATA_TABLE_COLUMN_WIDTHS = ((0, 30), (1, 150), (2, 70), (3, 150), (4, 49))
INFO_TABLE_COLUMN_WIDTHS = ((0, 32), (1, 68), (2, 68), (3, 68), (4, 40), (5, 52))
TARGET_TABLE_COLUMN_WIDTHS = ((0, 30), (1, 113), (2, 110), (3, 49), (4, 49), (5, 49), (6, 49))
FILES_TABLE_COLUMN_WIDTHS = ((0, 55), (1, 38), (2, 110), (3, 92), (4, 40), (5, 12))

# 复盘模块循环页各技能显示内容
available_buffs = {
    '分山劲': {
        '盾压': ['FenYe', 'XueNu', 'YuJian', 'JunXiao', 'CongRong', 'LianZhan'],
        '盾击': ['DaoHun', 'FenYe', 'XueNu', 'YuJian', 'JunXiao', 'CongRong', 'LianZhan'],
        '盾飞': ['DaoHun', 'FenYe', 'XueNu', 'YuJian', 'JunXiao', 'CongRong', 'LianZhan'],
        '斩刀': ['DaoHun', 'FenYe', 'XueNu', 'YuJian', 'JunXiao', 'CongRong', 'LianZhan'],
        '绝刀': ['FenYe', 'XueNu', 'YuJian', 'JunXiao', 'CongRong', 'LianZhan'],
        '阵云结晦': ['DaoHun', 'FenYe', 'XueNu', 'YuJian', 'JunXiao', 'CongRong', 'LianZhan'],
        '月照连营': ['FenYe', 'XueNu', 'YuJian', 'JunXiao', 'CongRong', 'LianZhan'],
        '雁门迢递': ['FenYe', 'XueNu', 'YuJian', 'JunXiao', 'CongRong', 'LianZhan']
    },
    '铁骨衣': {
        '盾刀': ['HanJia', 'LianZhan', 'DunDang', 'ChongYun', 'JianTie', 'Enchant_Belt', 'Enchant_Hat'],
        '盾击': ['HanJia', 'LianZhan', 'DunDang', 'ChongYun', 'JianTie', 'Enchant_Belt', 'Enchant_Hat'],
        '盾压': ['HanJia', 'LianZhan', 'DunDang', 'ChongYun', 'Enchant_Belt', 'Enchant_Hat'],
        '盾飞': ['HanJia', 'LianZhan', 'DunDang', 'ChongYun', 'Enchant_Belt', 'Enchant_Hat'],
        '斩刀': ['HanJia', 'LianZhan', 'DunDang', 'ChongYun', 'Enchant_Belt', 'Enchant_Hat'],
        '绝刀': ['HanJia', 'LianZhan', 'DunDang', 'ChongYun', 'Enchant_Belt', 'Enchant_Hat'],
        '盾挡': ['HanJia', 'LianZhan', 'DunDang', 'ChongYun', 'Enchant_Belt', 'Enchant_Hat'],
        '断马摧城': ['HanJia', 'LianZhan', 'DunDang', 'ChongYun', 'Enchant_Belt', 'Enchant_Hat'],
    }
}

available_specials = {
    '分山劲': {
        '盾压': ['count', 'yujian_rate'],
        '盾击': ['count', 'daohun_rate'],
        '盾飞': ['count', 'dunfei_rate'],
        '斩刀': ['count'],
        '绝刀': ['count', 'cw_count', 'norm_rage', 'cw_rage'],
        '阵云结晦': ['count', 'zhenyun_overflow'],
        '月照连营': ['count'],
        '雁门迢递': ['count', 'jueguo_count']
    },
    '铁骨衣': {
        '盾刀': ['count', 'hanjia_layer'],
        '盾击': ['count', 'hanjia_layer'],
        '盾压': ['count', 'hanjia_layer'],
        '盾飞': ['count', 'hanjia_layer'],
        '斩刀': ['count', 'hanjia_layer'],
        '绝刀': ['count', 'hanjia_layer'],
        '盾挡': ['count'],
        '断马摧城': ['count', 'hanjia_layer'],
    }
}

try:
    buff_icons = {
        'DaoHun': Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/刀魂.png', 'r'),
        'FenYe': Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/分野.png', 'r'),
        'CongRong': Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/从容.png', 'r'),
        'FengMing': Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/锋鸣.png', 'r'),
        'ChongYun': Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/崇云.png', 'r'),
        'JunXiao': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/军啸.png', 'r'),
        'Enchant_Hat': Image.open(r'Sources/Jx3_Datas/Icons/jx3basic_icons/enchant.png', 'r'),
        'XueNu': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/血怒.png', 'r'),
        'LianZhan': Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/恋战.png', 'r'),
        'HanJia': Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/寒甲.png', 'r'),
        'JianTie': Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/坚铁.png', 'r'),
        'YuJian': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/玉简·分山劲.png', 'r'),
        'CanJuan': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/残卷·铁骨衣.png', 'r'),
        'DunDang': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/盾挡.png', 'r'),
        'Enchant_Belt': Image.open(r'Sources/Jx3_Datas/Icons/jx3basic_icons/enchant.png', 'r'),
    }
except FileNotFoundError as e:
    raise SourceNotFoundError(f"Any {e}")

buff_to_name = {
    'DaoHun': '刀魂',
    'FenYe': '分野',
    'CongRong': '从容',
    'FengMing': '锋鸣',
    'ChongYun': '崇云',
    'JunXiao': '军啸',
    'Enchant_Hat': '御帽',
    'XueNu': '血怒',
    'LianZhan': '恋战',
    'HanJia': '寒甲',
    'JianTie': '坚铁',
    'YuJian': '玉简',
    'CanJuan': '残卷',
    'DunDang': '盾挡',
    'Enchant_Belt': '伤腰',
}

special_to_name = {
    'count': '次数',
    'norm_rage': '平均怒气',  # 非特效绝刀怒气
    'cw_rage': '橙武特效怒气',  # 特效绝刀怒气
    'cw_count': '特效绝刀数量',  # 特效绝刀数量
    'jueguo_count': '绝国比例',  # 绝国数量
    'dunfei_rate': '盾飞时间比率',  # 盾飞数量/时间
    'zhenyun_overflow': '阵云溢出层数',  # 阵云溢出层数
    'daohun_rate': '刀魂盾击比例',    # 刀魂盾击占盾回盾击比例
    'yujian_rate': '玉简盾压比例',    # 玉简盾压占总盾压比例
    'hanjia_layer': '寒甲平均层数',
}

special_to_type = {
    'count': 'int',
    'norm_rage': 'float',  # 非特效绝刀怒气
    'cw_rage': 'float',  # 特效绝刀怒气
    'cw_count': 'int',  # 特效绝刀数量
    'jueguo_count': 'float',  # 绝国数量
    'dunfei_rate': 'float',  # 盾飞数量/时间
    'zhenyun_overflow': 'int',  # 阵云溢出层数
    'daohun_rate': 'float',     # 刀魂盾击比例
    'yujian_rate': 'float',
    'hanjia_layer': 'int',
}

miss_to_name = {
    'DaoHun': '刀魂',
    'FenYe': '分野',
    'XueNu': '血怒',
    'YuJian': '玉简',
    'ZhenYun': '阵云'
}






