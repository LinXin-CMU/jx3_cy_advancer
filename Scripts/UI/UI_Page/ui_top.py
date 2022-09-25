# coding: utf-8
# author: LinXin
"""
ui首页的功能
"""
from os import getcwd, listdir, path
from re import compile, match
from shutil import move
from typing import Any
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QHeaderView, QTableWidgetItem, QAbstractItemView, QLabel
from PyQt5.QtCore import Qt, QTime
from time import localtime
from datetime import datetime, timedelta
from winreg import OpenKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE
from os import listdir, path
from lupa import LuaRuntime
from csv import DictWriter

from Scripts.UI.UI_Base.ui_base import BaseUi
from Scripts.UI.UI_Base.ui import Ui_MainWindow
from Scripts.UI.UI_Base.ui_other import FILES_TABLE_COLUMN_WIDTHS, set_page
from CustomClasses.Exceptions import NotFoundJclFolderError


set_row = set_page

f = open("log.txt", 'w', encoding='gbk')


class Top_UI(BaseUi):

    def __init__(self, obj: QMainWindow):
        super(Top_UI, self).__init__()
        # 基础定义
        self.ui: Ui_MainWindow = obj.ui
        self.widget = obj
        self.lua = LuaRuntime()
        # 角色名
        self.player_name = ''
        # 游戏路径
        self.game_path = None
        # 目标文件夹路径
        self.folder_path = None
        # 当前目标文件夹从属
        self._folder_from = None
        # 目标文件
        self._target_file = None
        # 待筛选的文件序列
        # 设置表格列宽
        for data in FILES_TABLE_COLUMN_WIDTHS:
            self.ui.top_files_table.setColumnWidth(*data)
        self.local_time = localtime()
        # 设置combobox数据
        self._set_nearest_date_combobox()
        # 将标定时间默认值设为5分钟
        self.ui.top_fight_time_timeedit.setTime(QTime(5, 0))
        # 读取config以初始化
        self._read_config()
        # 绑定控件
        self._widget_connection()
        # 过滤top_files_table被异常触发的问题
        self._trig = True
        # 初始化时隐藏提示
        self.ui.cue_label.hide()

        # 筛选器条件
        self._filter = {
            'date': Any,
            'type': Any
        }
        # 读取一次筛选器
        self._read_filter_condition()
        # 文件列表
        self._files = {
            'max_length': 50,
            'data': []
            # index, date, time, map, target, persist, name
        }
        # 设置列名显示
        self.ui.top_files_table.horizontalHeader().setVisible(True)

    @property
    def target_file(self):
        return self.ui.FileLineEdit.text()

    @property
    def run_data(self):
        """
        主函数用，复盘用文件路径和角色名
        :return:
        """
        # 确定运行后再记录目标文件名, 供导出csv用
        self._target_file = self.ui.FileLineEdit.text().rsplit('/', 1)[-1]
        return [self.player_name, self.ui.FileLineEdit.text()]

    def _widget_connection(self):
        """
        绑定控件的槽
        :return:
        """
        # 绑定按钮
        self.ui.SelectGamePath.clicked.connect(self._game_path_button_func)
        self.ui.SelectFile.clicked.connect(self._select_file_button_func)
        self.ui.top_filt_button.clicked.connect(self._get_all_jcl_files_from_folder)
        self.ui.open_garbage_button.clicked.connect(self._select_file_in_garbage_button_func)
        # 绑定文本框
        # 这里是检查手动输入的路径是否有误
        # 太无语了改一个字就会触发，在其他地方检查吧
        # self.ui.PathLineEdit.textChanged.connect(lambda: self._game_path_button_func(game_path=self.ui.PathLineEdit.text()))
        # 绑定角色名文本框
        self.ui.NameLineEdit.textChanged.connect(self._set_player_name)
        self.ui.PathLineEdit.textChanged.connect(self._set_game_path)
        # 绑定筛选条件
        self.ui.top_nearest_days_combobox.currentIndexChanged.connect(lambda: self.ui.radioButton.setChecked(True))
        self.ui.top_nearest_year_combobox.currentIndexChanged.connect(lambda: self.ui.radioButton_2.setChecked(True))
        self.ui.top_nearest_month_combobox.currentIndexChanged.connect(lambda: self.ui.radioButton_2.setChecked(True))
        self.ui.top_nearest_days_combobox.currentIndexChanged.connect(self._read_filter_condition)
        self.ui.top_nearest_year_combobox.currentIndexChanged.connect(self._read_filter_condition)
        self.ui.top_nearest_month_combobox.currentIndexChanged.connect(self._read_filter_condition)
        # 绑定按钮组
        self.ui.top_nearest_date_buttonGroup.buttonClicked.connect(self._read_filter_condition)
        self.ui.top_zone_type_buttonGroup.buttonClicked.connect(self._read_filter_condition)
        # 不可改变列宽
        # self.ui.top_files_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.top_files_table.setColumnHidden(7, True)
        self.ui.top_files_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 点击单选框触发
        # self.ui.top_files_table.cellChanged.connect(self._table_inside_button_func)
        # 点击该行触发
        self.ui.top_files_table.cellClicked.connect(self._table_inside_button_func)

    def _read_config(self):
        """
        初始化时尝试读取游戏路径\n
        :return:
        """
        global f
        f.write(f"row 137, inside _read_config\n")
        f.close()
        f = open('log.txt', 'a', encoding='gbk')

        _name = self.config['player_name']
        if _name is not None:
            self.player_name = _name
            self.ui.NameLineEdit.setText(self.player_name)
        _path = self.config['game_path']
        if _path is not None:
            self.game_path = _path
            self.ui.PathLineEdit.setText(self.game_path)
        else:
            # 尝试从注册表中读取游戏路径
            self._split_game_path(self._get_game_path())
            if self.game_path is None:
                self.ShowWarningBoxForNotFountJx3GameError(self.widget)
            else:
                self.ui.PathLineEdit.setText(self.game_path)
        # 尝试读取目标文件夹
        _folders = self.config['jcl_paths']
        if _folders is not None:
            _folders = eval(_folders)
            if self.player_name in _folders:
                self.folder_path = _folders[self.player_name]
                self._folder_from = self.player_name

    def _set_nearest_date_combobox(self):
        """
        根据当前年月设置top_nearest_year_combobox和top_nearest_month_combobox的选项\n
        :return:
        """
        year = self.local_time.tm_year
        month = self.local_time.tm_mon
        # 添加年份, 当前年份-2014
        self.ui.top_nearest_year_combobox.addItems([str(i) + "年" for i in range(year, 2013, -1)])
        # 添加月份, 当前月份-1
        self.ui.top_nearest_month_combobox.addItems([str(i) + "月" for i in range(month, 0, -1)])

    def _set_player_name(self):
        """
        设置游戏名的方法\n
        :return:
        """
        self.player_name = self.ui.NameLineEdit.text()
        self.config.add_config('main', 'player_name', self.player_name)

    def _split_game_path(self, origin_path: str):
        """
        把从不同渠道获取的游戏路径切分为标准路径并储存\n
        :return:
        """
        global f
        self.game_path = origin_path
        self.ui.PathLineEdit.setText(self.game_path)
        for _ in range(10000):
            try:
                if '\\' in origin_path:
                    origin_path = origin_path.replace('\\', '/')
                f.write(f'row 190, now path: {origin_path.__repr__()}\n')
                f.close()
                f = open('log.txt', 'a', encoding='gbk')
                _path = origin_path.rsplit("/", 1)
                if _path[1] in 'Game':
                    self.game_path = _path[0]
                    self.ui.PathLineEdit.setText(self.game_path)
                    self.config.add_config('main', 'game_path', self.game_path)
                    f.write(f'row 203, found from {origin_path.__repr__()}\n')
                    f.close()
                    f = open('log.txt', 'a', encoding='gbk')
                    break
                else:
                    origin_path = _path[0]
            except IndexError as e:
                print(f"IndexError: {e} at Scripts/UI/UI_Page/ui_top.py _game_path_button_func: 填写的剑网3游戏路径有误")
                break

    def _set_game_path(self):
        """
        从文本框读取游戏路径\n
        :return:
        """
        _text = self.ui.PathLineEdit.text()
        if '\\' in _text:
            _text = _text.replace('\\', '/')
        self.game_path = _text

    @staticmethod
    def _get_game_path():
        """
        通过读取注册表尝试获取游戏路径\n
        :return:
        """
        global f

        v = ''
        for regpath in [r'SOFTWARE\JX3Installer', r'SOFTWARE\Kingsoft\JX3', r'SOFTWARE\Kingsoft\SeasunGame\JX3']:
            try:
                key = OpenKey(HKEY_LOCAL_MACHINE, regpath)
                for i in range(50):
                    k, v, t = EnumValue(key, i)
                    f.write(f"row 229, {regpath}_{k}_{v}\n")
                    f.close()
                    f = open('log.txt', 'a', encoding='gbk')
                    if k == 'InstPath':
                        if '\\' in v:
                            v = v.replace("\\", "/")
                        v += '/Game'
                        CloseKey(key)
                        return v
                    elif k == 'InstallPath':
                        CloseKey(key)
                        return v
            except FileNotFoundError as e:
                f.write(f'cannot open path at {regpath}\n')
                f.close()
                f = open('log.txt', 'a', encoding='gbk')
                continue
        return v

    def _game_path_button_func(self):
        """
        手动选择游戏路径的方法\n
        :param game_path:
        :return:
        """
        global f
        f.write(f"row 137, inside _game_path_button_func\n")
        f.close()
        f = open('log.txt', 'a', encoding='gbk')
        game_path = QFileDialog.getExistingDirectory(self.widget, "请选择剑网3游戏文件夹下的Game文件夹")
        self._split_game_path(game_path)
        if self.game_path is None:
            self.ShowWarningBoxForJx3GamePathSelectError(self.widget)

    def _select_file_button_func(self):
        """
        手动选择jcl文件的方法\n
        :return:
        """
        self._get_player_jcl_folder_path()
        if self.folder_path is not None:
            _target_file = \
                QFileDialog.getOpenFileName(self.widget, '请选择想要复盘的文件', f'{self.folder_path}', 'Jcl战斗记录文件(*.jcl)')[0]
            self.ui.FileLineEdit.setText(_target_file)
        else:
            _target_file = \
                QFileDialog.getOpenFileName(self.widget, '请选择想要复盘的文件', f'{getcwd()}', 'Jcl战斗记录文件(*.jcl)')[0]
            self.ui.FileLineEdit.setText(_target_file)

    def _select_file_in_garbage_button_func(self):
        """
        在垃圾箱中手动选择jcl文件的方法\n
        :return:
        """
        _target_file = \
            QFileDialog.getOpenFileName(self.widget, '请选择想要复盘的文件', r"Sources/Jcl_Garbage", 'Jcl战斗记录文件(*.jcl)')[0]
        self.ui.FileLineEdit.setText(_target_file)

    def _table_inside_button_func(self, row: int, column: int):
        """
        绑定到表格内按钮的函数\n
        1.设置当前行\n
        2.取消选择其他所有按钮
        :param row:
        :param column:
        :return:
        """
        # 过滤设置时的被触发情况
        if not self._trig:
            return
        # if not column == 5:
        #     return
        # 0913添加删除功能
        if not column == 6:
            # 设置当前行
            key = self.ui.top_files_table.item(row, 7).text()
            self.ui.FileLineEdit.setText(f"{self.folder_path}/{key}")
            # 取消其他行
            print(row)
            self._trig = False
            for r in range(self.ui.top_files_table.rowCount()):
                if not r == row:
                    self.ui.top_files_table.item(r, 5).setCheckState(False)
                else:
                    # 对点击行的适配
                    self.ui.top_files_table.item(r, 5).setCheckState(True)
            self._trig = True
        else:
            self.del_file_button_func(row)

    def _get_player_jcl_folder_path(self):
        """
        根据游戏路径寻找到对应jcl文件夹路径的方法\n
        :return:
        """
        # if self.folder_path is None:
        _path = self.game_path + r'/Game/JX3/bin/zhcn_hd/interface/MY#DATA'
        # 遍历MY#DATA，找到与player_name相符的文件夹
        # 新版客户端适配
        if not path.exists(_path):
            _path = self.game_path + r'/Game/JX3_takeover/bin/zhcn_hd/interface/MY#DATA'
        # 均查询不到的情况下则遍历
        if not path.exists(_path):
            # 可能的目录
            possible = {'JX3', 'JX3_EXP', 'Game', 'JX3_takeover', 'bin', 'zhcn_hd', 'interface'}
            stop = 'MY#DATA'
            #
            _branches = [self.game_path]
            for _ in range(1000):
                cache = []
                for folder in _branches:
                    dirs = listdir(folder)
                    # 检查是否可能是目标文件夹
                    for _d in dirs:
                        if _d in possible and path.isdir(f"{folder}/{_d}"):
                            cache.append(f"{folder}/{_d}")
                        elif _d == stop and path.isdir(f"{folder}/{_d}"):
                            _path = f"{folder}/{_d}"
                            break
                if _path.endswith('MY#DATA') and path.isdir(_path):
                    break
                else:
                    _branches = [i for i in cache]

        if not path.exists(_path):
            self.ShowWarningBoxForJx3GamePathSelectError(self.widget)
            return
        for _folder in listdir(_path):
            try:
                if isinstance(eval(_folder.split('@')[0]), int):
                    # 找到存放玩家数据的文件夹
                    if self.player_name in listdir(rf'{_path}/{_folder}'):
                        _path += rf'/{_folder}/userdata/combat_logs'
                        self.folder_path = _path
                        self._folder_from = self.player_name
                        # print(self.folder_path)
                        self._add_config_jcl_path()
                        return
            except SyntaxError as e:
                print(
                    f"SyntaxError: {e} at Scripts/UI/UI_Page/ui_top.py _get_player_jcl_folder_path: 过滤MY#DATA中非玩家文件夹")
                continue
        else:
            self.ShowWarningBoxForIdNotInGamePath(self.widget)
            self.folder_path = None

    def _add_config_jcl_path(self):
        """
        写入当前id所对应的游戏路径\n
        :return:
        """
        # {name: path}
        _paths = self.config['jcl_paths']
        if _paths is not None:
            # print(type(_paths))
            _paths = eval(_paths)
            if path.exists(self.folder_path):
                # 校验路径是否存在，因为可能有手动填写的情况
                _paths[self.player_name] = self.folder_path
                self.config.add_config('main', 'jcl_paths', _paths)
        else:
            self.config.add_config('main', 'jcl_paths', {self.player_name: self.folder_path})

    def _read_filter_condition(self):
        """
        读取当前的筛选条件并写入属性\n
        :return:
        """
        button = self.ui.top_nearest_date_buttonGroup.checkedButton()
        if button.text() == '最近':
            self._filter['date'] = {'nearest_day': int(self.ui.top_nearest_days_combobox.currentText()[:-1])}
        else:
            self._filter['date'] = {'year': int(self.ui.top_nearest_year_combobox.currentText()[:-1]),
                                    'month': int(self.ui.top_nearest_month_combobox.currentText()[:-1])}
        self._filter['type'] = []
        buttons = self.ui.top_zone_type_buttonGroup.buttons()
        for button in buttons:
            if button.isChecked():
                self._filter['type'].append(button.text())

        # print(self._filter)

    def export_csv_data(self, data):
        """
        将当前记录导出为csv文件\n
        :return:
        """
        # 判断是否无数据
        if data is None:
            self.ShowWarningBoxForNotStartRead(self.widget)
        else:
            workpath = QFileDialog.getExistingDirectory(self.widget, "请选择想要保存到的目录", getcwd())
            csv_name = self._target_file.replace(".jcl", "-") + self.player_name + '.csv'
            try:
                with open(f"{workpath}/{csv_name}", 'w', encoding='gbk', newline='') as f:
                    csv_writer = DictWriter(f, fieldnames=["frame", "timestamp", "msec", "event_type", 'buff_type',
                                                           'event_level', 'event_layer', 'effect_damage', 'effect_health',
                                                           'caster_name', 'caster_id', 'target_name', 'target_id',
                                                           'type_name', 'type', 'event_name', 'event_id', 'iscritical',
                                                           "data"])
                    csv_writer.writeheader()
                    for item in data:
                        csv_writer.writerow(data[item])
                self.ShowInfoBoxForExportSuccess(self.widget, 'Excel')
            except PermissionError as e:
                print(f"Permission Error: {e} at Scripts/UI/UI_Page/ui_top.py export_csv_data: 目标文件已被打开")

    def _get_all_jcl_files_from_folder(self):
        """
        从文件夹中读取出jcl文件\n
        :return:
        """

        global f
        f.write(f'inside Top_UI._get_all_jcl_files_from_folder\n')
        f.close()
        f = open('log.txt', 'a', encoding='gbk')

        self._files = {
            'max_length': 50,
            'data': []
            # index, date, time, map, target, persist, name
        }
        self._trig = False

        # 新用户名点击的情况
        if self.folder_path is None:
            self._get_player_jcl_folder_path()
        # 使用时更改用户名的情况
        # 与上文不同时出现
        elif self.player_name != self._folder_from:
            self._get_player_jcl_folder_path()
        # 判断路径是否为None, 防止os.getcwd()的问题
        if self.folder_path is None:
            return

        f.write(f'row 467, {self.folder_path}\n')
        f.close()
        f = open('log.txt', 'a', encoding='gbk')

        # 路径不为None的情况下
        try:
            _files = listdir(self.folder_path)
            f.write(f'row 481, listdir\n')
            f.close()
            f = open('log.txt', 'a', encoding='gbk')
        except FileNotFoundError:
            raise NotFoundJclFolderError
        pattern = compile(
            r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<second>\d{2})-(?P<map>.*?)-(?P<boss>.*?)\.jcl')
        _current_zones = eval(self.config['jx3_zones'])
        f.write(f'row 490, reading\n')
        f.close()
        f = open('log.txt', 'a', encoding='gbk')
        for index, item in enumerate(_files):
            # 筛选器用的标签，代表符合其他条件，可以跳过“其他”筛选
            _pass = False
            # 过滤.log文件
            if item.endswith('.log'):
                continue
            f.write(f'row 494, matching {item}\n')
            f.close()
            f = open('log.txt', 'a', encoding='gbk')
            res = match(pattern, item)
            if res is None:
                continue
            # index, date, time, map, target, persist, name
            # 过滤存在问题的文件名,如2022-08-08-19-17-35-苍云-.jcl
            f.write(f'row 499, reading {item}\n')
            f.close()
            f = open('log.txt', 'a', encoding='gbk')
            if '' in res.groups():
                continue
            _year = int(res.group('year'))
            _month = int(res.group('month'))
            _day = int(res.group('day'))
            _hour = int(res.group('hour'))
            _minute = int(res.group('minute'))
            _map = res.group('map')
            _boss = res.group('boss')
            # 执行筛选条件
            f.write(f'row 515, filtrate {item}\n')
            f.close()
            f = open('log.txt', 'a', encoding='gbk')
            if self._filter['date'] is not Any:
                # 根据时间筛选
                _time_filter = self._filter['date']
                if 'nearest_day' in _time_filter:
                    _limit = datetime.now() - timedelta(days=_time_filter['nearest_day'])
                    _dist = datetime(year=_year, month=_month, day=_day, hour=_hour, minute=_minute, second=int(res.group('second'))) - _limit
                    if _dist.days < 0:
                        continue
                else:
                    if (_year != _time_filter['year']) or (_month != _time_filter['month']):
                        continue
            if self._filter['type'] is not Any:
                _type_filter = self._filter['type']
                # 根据副本类型筛选
                if '浪客行' in _map:
                    # 直接过滤浪客行
                    continue

                if '木桩' in _boss:
                    if '木桩' not in _type_filter:
                        continue
                    else:
                        _pass = True
                elif _map in _current_zones:
                    if '25人主流副本' not in _type_filter:
                        continue
                    else:
                        _pass = True
                elif '试炼之地' in _map:
                    if '试炼之地' not in _type_filter:
                        continue
                    else:
                        _pass = True
                else:
                    if '其它' not in _type_filter:
                        if not _pass:
                            continue

            # 新建对应行的单选按钮
            check_box = QTableWidgetItem()
            check_box.setCheckState(Qt.Unchecked)
            # 生成供ui选择后回溯的key
            # 用HiddenColumn代替
            # decode_key = f"{_year}{_month:02}{_day:02}{_hour:02}{_minute:02}"
            # 记录对应行
            # 新建对应行的删除按钮
            del_button = QLabel()
            del_button.resize(30, 15)
            del_button.setText('删除')
            del_button.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            del_button.setStyleSheet("font-size: 8pt; background-color: #e4976a; color: #ffffff")

            try:
                self._files['data'].append({
                    'date': f"{_year - 2000}/{_month:02}/{_day:02}",
                    'time': f"{_hour:02}:{_minute:02}",
                    'map': _map,
                    'target': _boss,
                    'persist': self._get_jcl_file_persist_time(item),
                    'button': check_box,
                    'del': del_button,
                    'name': item
                })
                f.write(f'row 581, appending {item}\n')
                f.close()
                f = open('log.txt', 'a', encoding='gbk')
            except UnicodeDecodeError as e:
                print(
                    f"UnicodeDecodeError: {e} at Scripts/UI/UI_Page/ui_top.py _get_all_jcl_files_from_folder: jcl文件未知错误")
                continue
        f.write(f'row 567, {self._files.__repr__()[:20]}\n')
        f.close()
        f = open('log.txt', 'a', encoding='gbk')
        # 先按时间排序，再按日期排序，保证双降序
        self._files['data'].sort(key=lambda i: i['time'], reverse=True)
        self._files['data'].sort(key=lambda i: i['date'], reverse=True)
        # 有显示问题
        # self.ui.top_files_table.sortByColumn(1, Qt.DescendingOrder)
        # self.ui.top_files_table.sortByColumn(0, Qt.DescendingOrder)
        # 隐藏提示
        self.ui.cue_label.hide()
        # 清空表格
        self.ui.top_files_table.setRowCount(0)
        length = len(self._files['data'])
        if length == 0:
            # 直接显示提示
            self.ui.cue_label.show()
        else:
            # 写入表格
            self.ui.top_files_table.setRowCount(length)
            for index, row in enumerate(self._files['data']):
                for idx, item in enumerate(list(row.values())):
                    # 0913 添加删除文件功能
                    # if idx == 6:
                    #     idx = 7
                    if idx == 6:
                        # item.clicked.connect(set_row(index, self.del_file_button_func))
                        self.ui.top_files_table.setCellWidget(index, idx, item)
                    else:
                        _item = QTableWidgetItem(item)
                        _item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.ui.top_files_table.setItem(index, idx, _item)
            self.ui.top_files_table.setColumnHidden(7, True)

        # 恢复单选按钮的绑定
        # self.ui.top_files_table.cellChanged.connect(self._table_inside_button_func)

        # 设置表格可以被触发
        self._trig = True


    def del_file_button_func(self, row):
        """
        删除按钮的作用方式
        :param row:
        :return:
        """
        _parent_table = self.ui.top_files_table

        if _parent_table.rowCount() == 0:
            return
        try:
            # 1. 将目标文件移动到垃圾文件夹
            key = self.ui.top_files_table.item(row, 7).text()
            _target_file = f"{self.folder_path}/{key}"
            move(_target_file, r"Sources/Jcl_Garbage")
            # 2. 删除该行
            _parent_table.removeRow(row)
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e} at Scripts/UI/UI_Page/ui_top.py del_file_button_func: 未查找到目标文件，未知错误！")


    def _get_jcl_file_persist_time(self, filename) -> str:
        """
        从文件的最后一行读取到战斗时间\n
        :return:
        """
        _path = self.folder_path + '/' + filename
        with open(_path, 'rb') as _f:
            _f.seek(-100, 2)
            _s = _f.readlines()[-1].strip().split()[-1]
            secs = self.lua.eval(_s.decode('gbk'))[3]
            str_time = str(timedelta(seconds=secs // 1000))

            return ":".join(str_time.split(':')[1:])

