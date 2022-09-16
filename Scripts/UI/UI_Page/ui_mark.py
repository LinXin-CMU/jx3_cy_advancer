# coding: utf-8
# author: LinXin
# 评分页


from Scripts.UI.UI_Base.ui_base import BaseUi
from Scripts.UI.UI_Base.ui import Ui_MainWindow
from Scripts.UI.UI_Base.ui_other import MARK_TABLE_COLUMN_WIDTHS


from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.Qt import QFont


SHORT_NAME_TO_NAME = {
    '云': '阵云结晦',
    '月': '月照连营',
    '雁': '雁门迢递',
    '斩': '斩刀',
    '绝': '绝刀'
}


class Marker_UI(BaseUi):

    def __init__(self, obj: QMainWindow):
        super().__init__()
        self.ui: Ui_MainWindow = obj.ui
        self.widget = obj
        # 设置主表列宽
        for item in MARK_TABLE_COLUMN_WIDTHS:
            self.ui.marker_table.setColumnWidth(*item)
        self.ui.marker_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def set_mark_table(self, data):
        """
        设置评分表\n
        :param data:
        :return:
        """
        if data is None:
            return

        _table = self.ui.marker_table
        # 1. 重新整理数据
        _data = {}
        _standard_total_dmg = {name: data[0][name]*data[1][name] for name in data[0].keys()}
        _real_total_dmg = {name: data[2][name]*data[3][name] for name in data[0].keys()}
        _standard_percents = {name: _standard_total_dmg[name]/sum(_standard_total_dmg.values()) for name in data[0].keys()}
        _real_mark = {name: round((_real_total_dmg[name]/_standard_total_dmg[name])*100, 2) for name in data[0].keys()}
        for skill in data[0]:
            _reshaped = {
                'mark': _real_mark[skill],
                'mark_rate': _standard_percents[skill],
                'standard_count': data[0][skill],
                'standard_dmg': data[1][skill],
                'real_count': data[2][skill],
                'real_dmg': data[3][skill]
            }
            _data[skill] = _reshaped
        # 2. 设置行数
        # 五个主要评分技能
        _table.setRowCount(len(_data))
        # 3. 填写内容
        for index, _skill in enumerate(_data.keys()):
            skill_name = SHORT_NAME_TO_NAME[_skill]
            skill_data = _data[_skill]
            items = [
                QTableWidgetItem(f"{skill_name}"),
                QTableWidgetItem(f"{skill_data['mark']}"),
                QTableWidgetItem(f"×{skill_data['mark_rate']:.02}"),
                QTableWidgetItem(f"{skill_data['standard_count']}"),
                QTableWidgetItem(f"{skill_data['real_count']}"),
                QTableWidgetItem(f"{int(skill_data['standard_dmg'])}"),
                QTableWidgetItem(f"{int(skill_data['real_dmg'])}")
            ]
            for idx in range(len(items)):
                items[idx].setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                items[idx].setFont(QFont('SimHei', 10))
                _table.setItem(index, idx, items[idx])


        print(_data)





































