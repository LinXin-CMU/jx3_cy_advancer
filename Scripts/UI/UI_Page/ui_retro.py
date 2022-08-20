import random
from typing import Dict, List, Literal
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QLabel
from PyQt5.QtCore import Qt, QPointF
import pyqtgraph as pg
import numpy as np

from Scripts.UI.UI_Base.ui_base import BaseUi
from Scripts.UI.UI_Base.ui import Ui_MainWindow
from Scripts.UI.UI_Base.ui_other import TABLE_COLUMN_WIDTHS, INFO_TABLE_COLUMN_WIDTHS, TARGET_TABLE_COLUMN_WIDTHS


class Retro_UI(BaseUi):

    def __init__(self, obj: QMainWindow):
        super(Retro_UI, self).__init__()
        # 基础定义
        self.ui: Ui_MainWindow = obj.ui
        self.widget = obj
        # 技能data
        self.skill_data = None
        # 主表最近一次点击的内容，用于在附表读取目标表时用
        self._nearest_clicked_name = None
        # 主表被点击时抑制一次副表更新
        # self._nearest_be_clicked = 0
        # 附表行号和id的对照
        self._target_table_id = []
        # pyqtgraph初始化
        self.ui.graphicsView.setBackground((247, 245, 243))
        self.ui.graphicsView.setMenuEnabled(False)
        self.ui.graphicsView.hideButtons()
        self.ui.graphicsView.setMouseEnabled(x=False, y=False)
        # self.ui.graphicsView.setStyleSheet("PlotWidget{border-radius: 8px}")
        # 设置坐标轴
        self.plot_items = self.ui.graphicsView.getPlotItem()
        self.plot_items.getViewBox().invertY(True)
        self.plot_items.getAxis("bottom").hide()
        left_axis = self.plot_items.getAxis("left")
        left_axis.setLabel('战斗时间(s)')
        top_axis = self.plot_items.getAxis("top")
        top_axis.setLabel('伤害量')
        top_axis.show()
        # 设置点击坐标点时的标签
        self.time_label = QLabel(self.ui.groupBox_4)
        self.damage_label = QLabel(self.ui.groupBox_4)
        self.target_label = QLabel(self.ui.groupBox_4)
        # self.time_label.move(560, 550)
        # self.damage_label.move(660, 550)
        # self.target_label.move(760, 550)
        for index, label in enumerate([self.time_label, self.damage_label, self.target_label]):
            label.resize(100, 16)
            label.move((index+5)*100+57, 550)
            label.setStyleSheet("QLabel{color: rgb(227, 91, 57);}")
        # 记录当前坐标点的数据，便于展示
        self._points_datas = {}
        # 记录已被设置过边框的坐标点，便于清楚
        self._points_clicked: List | None = None



        # 设置列宽
        for item in TABLE_COLUMN_WIDTHS:
            self.ui.Retro_skill_data_table.setColumnWidth(*item)
        for item in INFO_TABLE_COLUMN_WIDTHS:
            self.ui.Retro_skill_info_table.setColumnWidth(*item)
        for item in TARGET_TABLE_COLUMN_WIDTHS:
            self.ui.Retro_skill_target_table.setColumnWidth(*item)
        # 不可改变
        self.ui.Retro_skill_data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.Retro_skill_info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 绑定触发
        self.ui.Retro_skill_data_table.itemSelectionChanged.connect(lambda: self.set_skill_info_table('by_skill'))
        self.ui.Retro_skill_data_table.itemSelectionChanged.connect(self.set_skill_target_table)
        self.ui.Retro_skill_data_table.itemSelectionChanged.connect(self.draw_graph)
        self.ui.Retro_skill_target_table.itemSelectionChanged.connect(lambda: self.set_skill_info_table('by_target'))


    def _scatter_clicked(self, plot, points):
        norm_pen = pg.mkPen((121, 194, 225), width=2)
        crit_pen = pg.mkPen((254, 208, 129), width=2)
        # 标签取值为其中随机一个数据点
        random.shuffle(points)
        if self._points_clicked is None:
            pass
        else:
            for old_p in self._points_clicked:
                old_p.resetPen()
            self._points_clicked.clear()
        for p in points:
            # 数据点边框
            # print(p.pos())
            # print(plot.__dict__)
            if plot.opts['name'] == "命中":
                p.setPen(norm_pen)
            else:
                p.setPen(crit_pen)
            # p.setPen()
            if self._points_clicked is None:
                self._points_clicked = [p]
            else:
                self._points_clicked.append(p)

        # 标签数据
        point = points[-1]
        sec = round(point.pos()[1], 4)
        msec = self._points_datas[sec]
        target = self.skill_data[self._nearest_clicked_name]['_now_target'][msec]
        self.time_label.setText(f"{sec:.2f}s")
        self.damage_label.setText(f"{int(point.pos()[0])}")
        self.target_label.setText(target)



    def set_skill_data_table(self, data: Dict):
        """
        设置Retro_skill_data_table的方法\n
        :return:
        """
        # _skill = {
        #     'szName': str: {
        #         等级已被合并或拆分
        #         'dwID': set,
        #         'nCount': int,
        #         'nCritical': int,
        #         'nDodge': int,
        #         'tResult': {
        #             伤害类型已s被合并
        #             'normal': List,
        #             'critical': List
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
        #             }
        #         },
        #         'percentage': {
        #             'total': float,
        #             'critical': float,
        #             'dodge': float,
        #         }
        #     }
        # }
        self.skill_data = data
        table = self.ui.Retro_skill_data_table

        # table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 读取数据并排序
        _list = []
        for skill_name, skill_data in data.items():
            _list.append([str(i) for i in [skill_name, skill_data['nCount'], skill_data['result_final']['total'], f"{skill_data['percentage']['total']:.2%}"]])
        _list.sort(key=lambda i: int(i[2]), reverse=True)
        # 判断是否有偏离的无伤害技能
        for index, item in enumerate(reversed(_list)):
            if item[2] == '0':
                del _list[-(index+1)]
        # 再设置行数
        table.setRowCount(0)
        table.setRowCount(len(_list))
        # 填入数据
        for index, item in enumerate(_list):
            for idx, string in enumerate(item):
                cell = QTableWidgetItem(string)
                # cell.setTextAlignment(Qt.AlignVCenter)
                table.setItem(index, idx+1, cell)
            table.setItem(index, 0, QTableWidgetItem(str(index+1)))
        # 设置文本向左或右对齐
        # for row in range(table.rowCount()):
        #     table.item(row, 2).setTextAlignment(Qt.AlignLeft)
        #     table.item(row, 3).setTextAlignment(Qt.AlignVCenter)
        #
        #     table.item(row, 3).setTextAlignment(Qt.AlignRight)
        #     table.item(row, 4).setTextAlignment(Qt.AlignRight)
        # 计数设置为-1，便于初次点击时生效
        # self._nearest_be_clicked = -1
        # 清空所有附表
        self.ui.Retro_skill_target_table.setRowCount(0)
        self.ui.Retro_skill_info_table.clearContents()
        self.ui.graphicsView.clearPlots()
        # 重写表格内容
        for index, item in enumerate(['命中', '会心', '偏离']):
            self.ui.Retro_skill_info_table.setItem(index, 0, QTableWidgetItem(item))

    def set_skill_info_table(self, table_type: Literal["by_skill", "by_target"]):
        """
        设置Retro_skill_info_table的方法
        :return:
        """
        # 是否完成读取的标志
        write_in = False
        _normal_list = []
        _critical_list = []
        _dodge_list = []
        if table_type == 'by_skill':
            table = self.ui.Retro_skill_data_table
            try:
                szName = table.item(table.currentRow(), 1).text()
                self._nearest_clicked_name = szName
            except AttributeError as e:
                print(f"AttributeError: {e} at Scripts/UI/UI_Page/ui_retro.py set_skill_info_table: 过滤掉重新读取文件时异常触发的情况")
            else:
                # print(self.skill_data[szName])
                # 按技能分类的情况
                _data = self.skill_data[szName]
                _normal = _data['result_final']['normal']
                _critical = _data['result_final']['critical']
                _dodge = _data['result_final']['dodge']

                _normal_list = [_normal['min'], _normal['mean'], _normal['max'], _data['nCount']-_data['nCritical']-_data['nDodge'], f"{1-_data['percentage']['critical']-_data['percentage']['dodge']:.2%}"]
                _critical_list = [_critical['min'], _critical['mean'], _critical['max'], _data['nCritical'], f"{_data['percentage']['critical']:.2%}"]
                _dodge_list = [_dodge['min'], _dodge['mean'], _dodge['max'], _data['nDodge'], f"{_data['percentage']['dodge']:.2%}"]
                write_in = True
                # 抑制计数+1
                # self._nearest_be_clicked = min(self._nearest_be_clicked+1, 1)

        elif table_type == 'by_target':
            # 按目标分类的情况
            # 过滤异常调用
            if self._nearest_clicked_name is None:
                print(f"异常调用: Scripts/UI/UI_Page/ui_retro.py set_skill_info_table: 未点击主表时目标表被调用")
            elif len(self._target_table_id) == 0:
                print(f"异常调用: Scripts/UI/UI_Page/ui_retro.py set_skill_info_table: 未点击主表时目标表被调用")
            # 如果主表刚刚被点击一次
            # elif self._nearest_be_clicked:
            #     self._nearest_be_clicked = 0
            #     return
            else:
                target_id = self._target_table_id[self.ui.Retro_skill_target_table.currentRow()]
                _data = self.skill_data[self._nearest_clicked_name]['targets'][target_id]
                _normal = _data['normal']
                _critical = _data['critical']
                _dodge = _data['dodge']
                _total_count = _normal['nCount'] + _critical['nCount'] + _dodge['nCount']
                _normal_list = [_normal['min'], _normal['mean'], _normal['max'], _normal['nCount'], f"{_normal['nCount'] / _total_count:.2%}"]
                _critical_list = [_critical['min'], _critical['mean'], _critical['max'], _critical['nCount'], f"{_critical['nCount'] / _total_count:.2%}"]
                _dodge_list = [_dodge['min'], _dodge['mean'], _dodge['max'], _dodge['nCount'], f"{_dodge['nCount'] / _total_count:.2%}"]
                write_in = True

        else:
            # 过滤异常情况
            return
        if write_in:
            for index, _list in enumerate([_normal_list, _critical_list, _dodge_list]):
                for idx, item in enumerate(_list):
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignVCenter)
                    self.ui.Retro_skill_info_table.setItem(index, idx+1, cell)


    def set_skill_target_table(self):
        """
        设置Retro_skill_target_table的方法
        :return:
        """
        self._target_table_id.clear()
        table = self.ui.Retro_skill_data_table
        try:
            szName = table.item(table.currentRow(), 1).text()
        except AttributeError as e:
            print(f"AttributeError: {e} at Scripts/UI/UI_Page/ui_retro.py set_skill_info_table: 过滤掉重新读取文件时异常触发的情况")
        else:
            _data = self.skill_data[szName]['targets']
            _to_table = []
            for target, target_data in _data.items():
                if target_data['total'] == 0:
                    continue
                # 把id绑定在了列表最末尾，这样可以随着排序变化而变化
                _to_table.append([str(i) for i in [target_data['target_name'], target_data['total'], target_data['normal']['nCount'], target_data['critical']['nCount'], target_data['dodge']['nCount'], f"{target_data['total']/self.skill_data[szName]['result_final']['total']:.2%}", target]])
            _to_table.sort(key=lambda i: int(i[1]), reverse=True)
            for index, item in enumerate(reversed(_to_table)):
                if item[1] == '0':
                    del _to_table[-(index+1)]
            self.ui.Retro_skill_target_table.setRowCount(0)
            self.ui.Retro_skill_target_table.setRowCount(len(_to_table))
            for index, item in enumerate(_to_table):
                # 记录index对应的id
                self._target_table_id.append(int(item[-1]))
                # 去掉最末的id
                for idx, string in enumerate(item[:-1]):
                    cell = QTableWidgetItem(string)
                    # cell.setData(Qt.ToolTipRole, f"{target}")
                    # cell.setTextAlignment(Qt.AlignVCenter)
                    self.ui.Retro_skill_target_table.setItem(index, idx + 1, cell)
                self.ui.Retro_skill_target_table.setItem(index, 0, QTableWidgetItem(str(index + 1)))
                # self.ui.Retro_skill_target_table.item(index, 0).setData(Qt.ToolTipRole, f"{target}")

    def draw_graph(self):
        self._points_datas.clear()
        table = self.ui.Retro_skill_data_table
        try:
            szName = table.item(table.currentRow(), 1).text()
            self._nearest_clicked_name = szName
        except AttributeError as e:
            print(f"AttributeError: {e} at Scripts/UI/UI_Page/ui_retro.py set_skill_info_table: 过滤掉重新读取文件时异常触发的情况")
        else:
            normal: Dict = self.skill_data[szName]['tResult']['normal']
            critical: Dict = self.skill_data[szName]['tResult']['critical']
            # 计算所需绘制的坐标点
            # normal_y = list([round(i / 1000, 4) for i in normal.keys()])
            # critical_y = list([round(i / 1000, 4) for i in critical.keys()])
            normal_y = []
            critical_y = []
            for n_y in normal.keys():
                pos_y = round(n_y / 1000, 4)
                normal_y.append(pos_y)
                self._points_datas[pos_y] = n_y
            for c_y in critical.keys():
                pos_y = round(c_y / 1000, 4)
                critical_y.append(pos_y)
                self._points_datas[pos_y] = c_y
            normal_x = list(normal.values())
            critical_x = list(critical.values())
            # 开始绘制坐标点
            self.ui.graphicsView.clearPlots()
            cri = self.ui.graphicsView.plot(critical_x, critical_y, pen=None, symbol='o', symbolBrush=(227, 91, 57, 180), name="会心")
            nor = self.ui.graphicsView.plot(normal_x, normal_y, pen=None, symbol='s', symbolBrush=(80, 95, 118, 180), name="命中")
            # 绑定坐标点被点击事件
            cri.sigPointsClicked.connect(self._scatter_clicked)
            nor.sigPointsClicked.connect(self._scatter_clicked)
            # print(cri)
            # legend = pg.LegendItem((40, 30), offset=(240, 1), pen=None)
            # legend.setParentItem(self.plot_items)
            # legend.addItem(cri, "会心")
            # legend.addItem(nor, "命中")
            # 换页时清除已被点击的坐标点
            if self._points_clicked is not None:
                self._points_clicked.clear()



