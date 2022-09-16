"""
零散函数和变量
"""
from os import listdir
from PIL import Image
from collections import namedtuple

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
FILES_TABLE_COLUMN_WIDTHS = ((0, 65), (1, 48), (2, 220), (3, 142), (4, 50), (5, 10), (6, 60))
MARK_TABLE_COLUMN_WIDTHS = ((0, 104), (1, 103), (2, 103), (3, 103), (4, 103), (5, 105), (6, 105))

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
        '盾刀': ['count', 'hanjia_layer', 'dundao_1', 'dundao_2', 'dundao_3', 'dundao_4'],
        '盾击': ['count', 'hanjia_layer'],
        '盾压': ['count', 'hanjia_layer'],
        '盾飞': ['count', 'hanjia_layer', 'dunfei_rate'],
        '斩刀': ['count', 'hanjia_layer'],
        '绝刀': ['count', 'hanjia_layer', 'cw_count', 'norm_rage'],
        '盾挡': ['count'],
        '断马摧城': ['count', 'hanjia_layer', 'duanma_rage'],
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
        'DanDao': Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/残楼.png', 'r'),
        'FengLing': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/锋凌横绝五阵.png', 'r'),
        'XueYun': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/血云.png', 'r'),
        'TaiChu': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/太初社稷.png', 'r'),
        'ZhuQue': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/朱轩怀雀.png', 'r'),
        'XiuLuo': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/修罗鬼面.png', 'r'),
        'NiYan': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/十律守心·猊焰.png', 'r'),
        'AnHun': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/十律守心·犴魂.png', 'r'),
        'BaiLang': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/白狼河北.png', 'r'),
        'BianSheng': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/四面边声.png', 'r'),
        'ZhanMa': Image.open(r'Sources/Jx3_Datas/Icons/buff_icons/斩马刑天.png', 'r'),
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
    'dundao_1': '一段盾刀数量',
    'dundao_2': '二段盾刀数量',
    'dundao_3': '三段盾刀数量',
    'dundao_4': '四段盾刀数量',
    'duanma_rage': '平均怒气',
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
    'dundao_1': 'int',
    'dundao_2': 'int',
    'dundao_3': 'int',
    'dundao_4': 'int',
    'duanma_rage': 'float',
}

miss_to_name = {
    'DaoHun': '刀魂',
    'FenYe': '分野',
    'XueNu': '血怒',
    'YuJian': '玉简',
    'ZhenYun': '阵云'
}

skill_icons = {}
try:
    files = listdir(r'Sources/Jx3_Datas/Icons/skill_icons')
    for file in files:
        name, ftype = file.split('.')
        if ftype == 'png':
            skill_icons[name] = Image.open(rf'Sources/Jx3_Datas/Icons/skill_icons/{file}', 'r')
except FileNotFoundError as e:
    raise SourceNotFoundError(f"Any {e}")
# print(skill_icons)


school_colors = {
    # light | dark
    'PengLai': ['#abe3fa', '#5d617e'],
    'BaDao': ['#6a6cbd', '#31276e'],
    'TianCe': ['#ff6f53', '#690e0e'],
    'GaiBang': ['#cd853f', '#9f6625'],
    'LingXue': ['#ee0d32', '#a10922'],
    'JiangHu': ['#ffffff', '#989898'],
    'CangJian': ['#d6f95d', '#94981b'],
    'CangYun': ['#de4a00', '#9d2f02'],
    'ShaoLin': ['#ffb25f', '#7d700a'],
    'YanTian': ['#a653fb', '#602d94'],
    'TangMen': ['#79b736', '#4b7128'],
    'ChangGe': ['#64fab4', '#1f7867'],
    'ChunYang': ['#16d8d8', '#085a71'],
    'QiXiu': ['#ff81b0', '#a24a81'],
    'WanHua': ['#c498ff', '#2f0e46'],
    'WuDu': ['#3793ff', '#07529a'],
    'MingJiao': ['#f04669', '#915011'],
    'YaoZong': ['#09b5a2', '#0a5157']
}







