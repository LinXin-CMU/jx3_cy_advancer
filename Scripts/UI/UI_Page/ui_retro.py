import datetime
import random
from typing import Dict, List, Literal
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QLabel, QPushButton, QHBoxLayout, \
    QVBoxLayout, QWidget, QFrame, QTableWidget, QHeaderView
from PyQt5.QtCore import Qt, QPointF, QSize
from PyQt5.Qt import QFont
from PIL import Image
import pyqtgraph as pg
import numpy as np

from Scripts.UI.UI_Base.ui_base import BaseUi
from Scripts.UI.UI_Base.ui import Ui_MainWindow
from Scripts.UI.UI_Base.ui_other import DATA_TABLE_COLUMN_WIDTHS, INFO_TABLE_COLUMN_WIDTHS, TARGET_TABLE_COLUMN_WIDTHS, \
    set_page, available_buffs, available_specials, buff_icons, buff_to_name, special_to_name, special_to_type, miss_to_name
from CustomClasses.Exceptions import SourceNotFoundError
from CustomClasses.jx3_collections import position, size


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
        # TabWidget基本设置
        # self.ui.tabWidget.setLayoutDirection(Qt.RightToLeft)
        self.ui.tabWidget.setAttribute(Qt.WA_StyledBackground)
        self.ui.tabWidget.setCurrentIndex(0)
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
            label.move((index + 5) * 100 + 57, 690)
            label.setStyleSheet("QLabel{color: rgb(227, 91, 57);}")
        # 记录当前坐标点的数据，便于展示
        self._points_datas = {}
        # 记录已被设置过边框的坐标点，便于清楚
        self._points_clicked: List | None = None
        # ----------循环页------------
        # 循环页图标
        self._major_skill_icon_labels = None
        # 右侧的图标
        self._major_buff_labels = None

        # 设置列宽
        for item in DATA_TABLE_COLUMN_WIDTHS:
            self.ui.Retro_skill_data_table.setColumnWidth(*item)
        for item in INFO_TABLE_COLUMN_WIDTHS:
            self.ui.Retro_skill_info_table.setColumnWidth(*item)
        for item in TARGET_TABLE_COLUMN_WIDTHS:
            self.ui.Retro_skill_target_table.setColumnWidth(*item)
        # 不可改变
        self.ui.Retro_skill_data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.Retro_skill_data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.Retro_skill_info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.Retro_skill_info_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.Retro_skill_target_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.Retro_skill_target_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # 绑定触发
        self.ui.Retro_skill_data_table.itemSelectionChanged.connect(lambda: self.set_skill_info_table('by_skill'))
        self.ui.Retro_skill_data_table.itemSelectionChanged.connect(self.set_skill_target_table)
        self.ui.Retro_skill_data_table.itemSelectionChanged.connect(self.draw_graph)
        self.ui.Retro_skill_target_table.itemSelectionChanged.connect(lambda: self.set_skill_info_table('by_target'))
        # 隐藏小标签
        for i in range(8):
            getattr(self.ui, f"miss_label_{i}").setVisible(False)
            getattr(self.ui, f"time_label_{i}").setVisible(False)

    # --------------复盘页---------------

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
            _list.append([str(i) for i in [skill_name, skill_data['nCount'], skill_data['result_final']['total'],
                                           f"{skill_data['percentage']['total']:.2%}"]])
        _list.sort(key=lambda i: int(i[2]), reverse=True)
        # 判断是否有偏离的无伤害技能
        for index, item in enumerate(reversed(_list)):
            if item[2] == '0':
                del _list[-(index + 1)]
        # 再设置行数
        table.setRowCount(0)
        table.setRowCount(len(_list))
        # 填入数据
        for index, item in enumerate(_list):
            for idx, string in enumerate(item):
                cell = QTableWidgetItem(string)
                # cell.setTextAlignment(Qt.AlignVCenter)
                table.setItem(index, idx + 1, cell)
            table.setItem(index, 0, QTableWidgetItem(str(index + 1)))
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

                _normal_list = [_normal['min'], _normal['mean'], _normal['max'],
                                _data['nCount'] - _data['nCritical'] - _data['nDodge'],
                                f"{1 - _data['percentage']['critical'] - _data['percentage']['dodge']:.2%}"]
                _critical_list = [_critical['min'], _critical['mean'], _critical['max'], _data['nCritical'],
                                  f"{_data['percentage']['critical']:.2%}"]
                _dodge_list = [_dodge['min'], _dodge['mean'], _dodge['max'], _data['nDodge'],
                               f"{_data['percentage']['dodge']:.2%}"]
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
                _normal_list = [_normal['min'], _normal['mean'], _normal['max'], _normal['nCount'],
                                f"{_normal['nCount'] / _total_count:.2%}"]
                _critical_list = [_critical['min'], _critical['mean'], _critical['max'], _critical['nCount'],
                                  f"{_critical['nCount'] / _total_count:.2%}"]
                _dodge_list = [_dodge['min'], _dodge['mean'], _dodge['max'], _dodge['nCount'],
                               f"{_dodge['nCount'] / _total_count:.2%}"]
                write_in = True

        else:
            # 过滤异常情况
            return
        if write_in:
            for index, _list in enumerate([_normal_list, _critical_list, _dodge_list]):
                for idx, item in enumerate(_list):
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignVCenter)
                    self.ui.Retro_skill_info_table.setItem(index, idx + 1, cell)

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
                _to_table.append([str(i) for i in
                                  [target_data['target_name'], target_data['total'], target_data['normal']['nCount'],
                                   target_data['critical']['nCount'], target_data['dodge']['nCount'],
                                   f"{target_data['total'] / self.skill_data[szName]['result_final']['total']:.2%}",
                                   target]])
            _to_table.sort(key=lambda i: int(i[1]), reverse=True)
            for index, item in enumerate(reversed(_to_table)):
                if item[1] == '0':
                    del _to_table[-(index + 1)]
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
            cri = self.ui.graphicsView.plot(critical_x, critical_y, pen=None, symbol='o',
                                            symbolBrush=(227, 91, 57, 180), name="会心")
            nor = self.ui.graphicsView.plot(normal_x, normal_y, pen=None, symbol='s', symbolBrush=(80, 95, 118, 180),
                                            name="命中")
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

    # --------------循环页---------------

    def set_school_operate_info(self, data):
        """
        设置循环页部分\n
        :param data: Dict{'major_skill_list', 'analysis', 'operate_list'}
        :return:
        """
        if data['major_skill_list'] is None:
            return
        skill_analysis = data['analysis']
        operate_list = data['operate_list']

        ICON_POS_X = (20, 240)
        ICON_POS_Y = (20, 93, 166, 240)
        ICON_SIZE = (40, 40)
        NAME_SIZE = QSize(111, 21)
        BUTTON_SIZE = QSize(201, 61)
        MISS_SIZE = QSize(20, 12)
        DELAY_SIZE = QSize(70, 12)
        # 左侧技能信息label相对于图标label的坐标
        NAME_LABEL_POS = position(60, 0)
        MISS_LABEL_POS = position(95, 30)
        DELAY_LABEL_POS = position(155, 30)
        BUTTON_POS = position(0, 0)

        ICON_PATH = r'Sources/Jx3_Datas/Icons/skill_icons'

        # 左侧技能图标边框
        try:
            # border = Image.open(r'Sources/Jx3_Datas/Icons/jx3basic_icons/border_qx.png')
            border = Image.open(r'Sources/Jx3_Datas/Icons/jx3basic_icons/orange.png')
            border = border.resize(ICON_SIZE)
            _, _, _, border_mask = border.split()
        except FileNotFoundError:
            raise SourceNotFoundError("border_qx.png")

        # 生成左侧labels
        if self._major_skill_icon_labels is None or len(self._major_skill_icon_labels) != 8:
            self._major_skill_icon_labels = None
            for index in range(len(data['major_skill_list'])):
                # 先放好label，在下方填数据
                x_idx, y_idx = divmod(index, 4)
                pos_y = ICON_POS_Y[y_idx]
                pos_x = ICON_POS_X[x_idx]
                # 图标
                icon_label = QLabel(self.ui.groupBox_5)
                icon_label.move(pos_x, pos_y)
                icon_label.resize(QSize(*ICON_SIZE))
                icon_label.setStyleSheet("border-radius: 3px;")
                # 技能名
                name_label = QLabel(self.ui.groupBox_5)
                name_label.move(pos_x + NAME_LABEL_POS.x, pos_y + NAME_LABEL_POS.y)
                name_label.resize(NAME_SIZE)
                name_label.setStyleSheet("font-size: 11pt;")
                # 失误
                miss_Label = QLabel(self.ui.groupBox_5)
                miss_Label.move(pos_x + MISS_LABEL_POS.x, pos_y + MISS_LABEL_POS.y)
                miss_Label.resize(MISS_SIZE)
                miss_Label.setStyleSheet("font-size: 9pt; color: rgb(236, 99, 65)")
                # 用时
                delay_label = QLabel(self.ui.groupBox_5)
                delay_label.move(pos_x + DELAY_LABEL_POS.x, pos_y + DELAY_LABEL_POS.y)
                delay_label.resize(DELAY_SIZE)
                delay_label.setStyleSheet("font-size: 9pt; color: rgb(236, 99, 65)")
                # 先放入Layout，再填入按钮
                # _button_layout_left = QHBoxLayout()
                # _button_layout_left.addWidget(getattr(self.ui, f"miss_label_{index}"))
                # _button_layout_left.addWidget(miss_Label)
                # _button_layout_right = QHBoxLayout()
                # _button_layout_right.addWidget(getattr(self.ui, f"time_label_{index}"))
                # _button_layout_right.addWidget(delay_label)
                # _button_layout = QHBoxLayout()
                # _button_layout.addLayout(_button_layout_left)
                # _button_layout.addLayout(_button_layout_right)
                _button_layout = QHBoxLayout()
                _lb = getattr(self.ui, f"miss_label_{index}")
                _lb.setVisible(True)
                _button_layout.addWidget(_lb)
                _button_layout.addWidget(miss_Label)
                _lb = getattr(self.ui, f"time_label_{index}")
                _lb.setVisible(True)
                _button_layout.addWidget(_lb)
                _button_layout.addWidget(delay_label)
                _right_layout = QVBoxLayout()
                _right_layout.addSpacing(2)
                _right_layout.addWidget(name_label)
                _right_layout.addSpacing(6)
                _right_layout.addLayout(_button_layout)
                _right_layout.addSpacing(2)
                layout = QHBoxLayout()
                layout.addWidget(icon_label)
                layout.addSpacing(10)
                layout.addLayout(_right_layout)

                # 先添加用于右侧翻页的透明按钮
                button = QPushButton(self.ui.groupBox_19)
                button.resize(BUTTON_SIZE)
                button.move(pos_x + BUTTON_POS.x, pos_y + BUTTON_POS.y)
                button.setStyleSheet("""
                QPushButton{
                    background-color: rgb(241, 239, 237);
                }
                QPushButton:hover{
                    background-color: rgb(235, 233, 231);
                    border: 1px solid rgb(213, 213, 213);
                    border-top: 2px solid rgb(213, 213, 213);
                    border-left: 2px solid rgb(213, 213, 213);
                }
                                """)
                button.setLayout(layout)
                button.clicked.connect(set_page(index, self.ui.tabWidget_2.setCurrentIndex))

                if self._major_skill_icon_labels is not None:
                    self._major_skill_icon_labels.append((icon_label, name_label, miss_Label, delay_label))
                else:
                    self._major_skill_icon_labels = [(icon_label, name_label, miss_Label, delay_label)]

        # 添加到左侧技能图标
        for index, labels in enumerate(self._major_skill_icon_labels):
            icon_label, name_label, miss_Label, delay_label = labels
            name = data['major_skill_list'][index]
            analysis_data = skill_analysis[name]
            # data =
            # 设置图标
            try:
                img = Image.open(rf'{ICON_PATH}/{name}.png')
                img = img.resize(ICON_SIZE)
                img.paste(border, mask=border_mask)
                icon_label.setPixmap(img.toqpixmap())
            except FileNotFoundError:
                raise SourceNotFoundError(f"{name}.png")
            # 设置名称
            name_label.setText(name)
            # 设置失误
            miss_Label.setText(f"{analysis_data['Miss']['total']}")
            # 设置用时
            delay_label.setText(f"{int(analysis_data['Special']['delay'])}ms".ljust(6))
        # print(skill_analysis)
        # print(operate_list)
        # 开始设置右侧
        # 先生成labels
        # 坐标直接写了
        if self._major_buff_labels is None or len(self._major_buff_labels) != 8:
            for index in range(len((data['major_skill_list']))):
                widget = getattr(self.ui, f"buffs_tab_{index}")
                # 竖线
                _line = QFrame(widget)
                _line.setFrameStyle(QFrame.VLine | QFrame.Sunken)
                _line.resize(20, 231)
                _line.move(110, 40)
                _line = QFrame(widget)
                _line.setFrameStyle(QFrame.VLine | QFrame.Sunken)
                _line.resize(20, 231)
                _line.move(250, 40)
                # 标题
                name_label = QLabel(widget)
                name_label.move(10, 10)
                name_label.resize(361, 20)
                name_label.setStyleSheet("font-size: 12pt;")
                name_label.setAlignment(Qt.AlignHCenter)
                # 表头
                _lb = QLabel("基础信息", widget)
                _lb.move(15, 40)
                _lb.resize(91, 16)
                _lb.setAlignment(Qt.AlignHCenter)
                _lb = QLabel("覆盖率", widget)
                _lb.move(140, 40)
                _lb.resize(111, 16)
                _lb.setAlignment(Qt.AlignHCenter)
                _lb = QLabel("失误时间", widget)
                _lb.move(285, 40)
                _lb.resize(71, 16)
                _lb.setAlignment(Qt.AlignHCenter)
                # 信息
                _infos = {}
                for idx in range(4):
                    _name_lb = QLabel(widget)
                    _name_lb.resize(71, 18)
                    _name_lb.setVisible(False)
                    _name_lb.setStyleSheet("font-size:9pt;")
                    _data_lb = QLabel(widget)
                    _data_lb.resize(31, 18)
                    _data_lb.setVisible(False)
                    _data_lb.setStyleSheet("font-size: 9pt; color: rgb(236, 99, 65)")
                    _data_lb.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    _infos[idx] = [_name_lb, _data_lb]

                # 表格
                time_table = QTableWidget(widget)
                time_table.move(275, 70)
                time_table.resize(91, 181)
                time_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                time_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                time_table.setColumnCount(2)
                time_table.setColumnWidth(0, 37)
                time_table.setColumnWidth(1, 32)
                time_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
                time_table.horizontalHeader().setVisible(False)
                time_table.verticalHeader().setVisible(False)
                time_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                time_table.setSelectionBehavior(QAbstractItemView.SelectRows)
                # 每一组
                _lbs = {}
                for _bf_label_count in range(7):
                    icon_label = QLabel(widget)
                    icon_label.resize(18, 18)
                    icon_label.setVisible(False)
                    buff_name_label = QLabel(widget)
                    buff_name_label.resize(61, 18)
                    buff_name_label.setVisible(False)
                    buff_data_label = QLabel(widget)
                    buff_data_label.resize(61, 18)
                    buff_data_label.setStyleSheet("color: rgb(236, 99, 65)")
                    buff_data_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    buff_data_label.setVisible(False)
                    _lbs[_bf_label_count] = [icon_label, buff_name_label, buff_data_label]

                if self._major_buff_labels is None:
                    self._major_buff_labels = [{
                        'name': name_label,
                        'info': _infos,
                        'buffs': _lbs,
                        'widget': widget,
                        'timetable': time_table,
                    }]

                else:
                    self._major_buff_labels.append({
                        'name': name_label,
                        'info': _infos,
                        'buffs': _lbs,
                        'widget': widget,
                        'timetable': time_table,
                    })
        # 填入右侧信息
        # 检查心法
        if '断马摧城' in data['major_skill_list']:
            kungfu = '铁骨衣'
        else:
            kungfu = '分山劲'

        # 取出对应buff序列
        if kungfu in available_buffs:
            _available_buff = available_buffs[kungfu]
            _available_info = available_specials[kungfu]
        else:
            print("未知问题 at Scripts/UI/UI_Page/ui_retro.py line 581")
            return
        _bf_count = len(_available_buff)

        # 取出buff边框
        try:
            # border = Image.open(r'Sources/Jx3_Datas/Icons/jx3basic_icons/border_qx.png')
            border = Image.open(r'Sources/Jx3_Datas/Icons/jx3basic_icons/orange.png')
            border = border.resize((18, 18))
            _, _, _, border_mask = border.split()
        except FileNotFoundError:
            raise SourceNotFoundError("border_qx.png")

        for index, sk_name in enumerate(data['major_skill_list']):
            labels = self._major_buff_labels[index]
            # 填入名称
            labels['name'].setText(f"{sk_name} 操作细节")
            # for idx, bf_label in enumerate(labels['buffs']):
            #     # 填入buff
            #     if idx > _bf_count - 1:
            #         # 清除后续的内容
            #         labels['buffs']
            # 获取到当前技能的所需展示buff
            if sk_name in _available_buff:
                _bf_lst = _available_buff[sk_name]
                _if_lst = _available_info[sk_name]
            else:
                print("未知问题 at Scripts/UI/UI_Page/ui_retro.py line 596")
                return
            # 开始填入右侧中央内容
            for idx, bf_labels in enumerate(labels['buffs'].values()):
                # 当前buff名称
                if idx < len(_bf_lst):
                    bf_name = _bf_lst[idx]
                    try:
                        bf_data = skill_analysis[sk_name]['Buffs'][bf_name]
                    except KeyError as e:
                        print(f"KeyError: {e} at Scripts/UI/UI_Page/ui_retro.py set_school_operate_info: 当前技能或buff并不属于要展示的buff")
                        return
                    bf_y = 70 + 26 * idx
                    # 取出对应icon并添加边框
                    try:
                        img = buff_icons[bf_name].resize((18, 18))
                        img.paste(border, mask=border_mask)
                    except KeyError as e:
                        print(f"KeyError: {e} at Scripts/UI/UI_Page/ui_retro.py set_school_operate_info: 当前buff并不属于要展示的buff")
                        return
                    # 设置对应icon
                    bf_labels[0].setPixmap(img.toqpixmap())
                    bf_labels[0].move(135, bf_y)
                    bf_labels[0].setVisible(True)
                    # 设置icon名称
                    try:
                        _name = buff_to_name[bf_name]
                    except KeyError as e:
                        print(f"KeyError: {e} at Scripts/UI/UI_Page/ui_retro.py set_school_operate_info: 当前buff并不属于要展示的buff")
                        return
                    bf_labels[1].setText(_name)
                    bf_labels[1].move(160, bf_y)
                    bf_labels[1].setVisible(True)
                    # 设置对应值
                    bf_labels[2].setText(f"{bf_data:.2f}")
                    bf_labels[2].move(190, bf_y)
                    bf_labels[2].setVisible(True)
                else:
                    for label in bf_labels:
                        label.setVisible(False)

            # 开始填入右侧左侧内容
            for idx, info_labels in enumerate(labels['info'].values()):
                if idx < len(_if_lst):
                    info_name = _if_lst[idx]
                    try:
                        info_data = skill_analysis[sk_name]['Special'][info_name]
                    except KeyError as e:
                        print(
                            f"KeyError: {e} at Scripts/UI/UI_Page/ui_retro.py set_school_operate_info: 当前技能或buff并不属于要展示的buff")
                        return
                    info_y = 70 + 26 * idx

                    # 设置icon名称
                    try:
                        _name = special_to_name[info_name]
                        _value_type = special_to_type[info_name]
                    except KeyError as e:
                        print(
                            f"KeyError: {e} at Scripts/UI/UI_Page/ui_retro.py set_school_operate_info: 当前buff并不属于要展示的buff")
                        return
                    info_labels[0].setText(_name)
                    info_labels[0].move(7, info_y)
                    info_labels[0].setVisible(True)
                    # 设置对应值
                    if _value_type == 'float':
                        info_labels[1].setText(f"{info_data:.2f}")
                    else:
                        info_labels[1].setText(f"{int(info_data)}")
                    info_labels[1].move(80, info_y)
                    info_labels[1].setVisible(True)
                else:
                    for label in info_labels:
                        label.setVisible(False)

            # 开始填入右侧表格内容
            tb = labels['timetable']

            for miss_name, miss_times in skill_analysis[sk_name]['Miss'].items():
                if miss_name == 'total':
                    continue
                if miss_name in miss_to_name:
                    name = miss_to_name[miss_name]
                else:
                    name = ""
                if len(miss_times) > 0:
                    for time in miss_times:
                        _, mm, _s = datetime.timedelta(seconds=time/1000).__str__().split(':')
                        ss, ms = _s.split(".")
                        time_item = QTableWidgetItem(f"{mm}:{ss}")
                        time_item.setFont(QFont("SimHei", 8, QFont.Normal))
                        name_item = QTableWidgetItem(name)
                        name_item.setFont(QFont("SimHei", 8, QFont.Normal))
                        name_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        tb.insertRow(tb.rowCount())
                        tb.setItem(tb.rowCount()-1, 0, time_item)
                        tb.setItem(tb.rowCount()-1, 1, name_item)
