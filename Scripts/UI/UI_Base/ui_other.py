"""
零散函数和变量
"""


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