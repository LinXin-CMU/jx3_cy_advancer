# coding: utf-8
# author: LinXin
# 复盘图片制作

from PyQt5.QtWidgets import QLabel, QFrame, QGroupBox
from PyQt5.Qt import QColor, QSize
from PyQt5.QtCore import QPoint
from PIL import Image
from collections import namedtuple, Iterable
from typing import Literal

from Scripts.UI.UI_Base.ui_other import buff_icons

position = namedtuple('position', ['x', 'y'])
size = namedtuple('size', ['w', 'h'])
row = namedtuple('row_data', ['name', 'top_y', 'height'])

# 一次绘图中添加的所有frames
frames = None


class Jx3Label(QLabel):
    # 自定义一个QLabel, 重写move方法
    def move(self, x) -> None:
        super(Jx3Label, self).move(QPoint(x, 0))


def _write_in(func):
    """
    用于记录当前添加的所有label
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        global frames
        ret = func(*args, **kwargs)
        if not isinstance(ret, Iterable):
            ret = [ret]
        for item in ret:
            if frames is None:
                frames = [item]
            else:
                frames.append(item)
    return wrapper



class OperatePainter:

    def __init__(self, parent: QGroupBox):
        self._parent = parent
        self._rows = {}
        self._lines = None
        self._set_rows()


    def _set_rows(self):
        """
        初始化时生成每一行的GroupBox和分界线
        :return:
        """
        ROWS = {
            0: row('时间轴', 130, 15),
            1: row('技能轴', 145, 60)
        }
        # 顶线

        def get_line() -> QFrame:
            _line = QFrame(self._parent)
            _line.setFrameStyle(QFrame.HLine | QFrame.Plain)
            _line.setLineWidth(2)
            _line.resize(10, 2)
            _line.setStyleSheet("background-color: rgb(0, 0, 0);")
            return _line

        row_tp = None
        for row_tp in ROWS.values():
            # 每行的groupbox
            _gb = QGroupBox(self._parent)
            _gb.resize(10, row_tp.height)
            _gb.move(0, row_tp.top_y)
            _gb.setVisible(False)
            # 每行的line
            _line = get_line()
            _line.move(0, row_tp.top_y - 1)
            _line.setVisible(False)
            # 储存
            self._rows[row_tp.name] = _gb
            if self._lines is None:
                self._lines = [_line]
            else:
                self._lines.append(_line)
        # 最后一行行尾的线
        if row_tp is not None:
            _line = get_line()
            _line.move(0, row_tp.top_y + row_tp.height - 1)
            _line.setVisible(False)
            if self._lines is None:
                self._lines = [_line]
            else:
                self._lines.append(_line)


    def _new_icon_label(self, row_name: str, icon_name: str | QColor, *, icon_type: Literal["buff", None] = None) -> QLabel:
        """
        返回一个新的在指定行的QLabel
        :param row_name:
        :return:
        """

        if row_name in self._rows:
            _parent = self._rows[row_name]
            _h = _parent.height()
        else:
            raise KeyError(f"行名称错误：{row_name}")

        _lb = Jx3Label(_parent)
        _lb.resize(_h, _h)

        if isinstance(icon_name, str):
            try:
                if icon_type is None:
                    img = Image.open(rf'Sources/Jx3_Datas/Icons/skill_icons/{icon_name}.png')
                else:
                    img = Image.open(rf'Sources/Jx3_Datas/Icons/buff_icons/{icon_name}.png')
            except FileNotFoundError:
                print(f"未查询到图标：{icon_name}.png")
                _lb.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 3px;")
                return _lb
            else:
                img = img.resize(_h, _h)
                _lb.setStyleSheet("border-radius: 3px;")
                _lb.setPixmap(img.toqpixmap())
                return _lb
        else:
            _lb.setStyleSheet(f"background-color: rgb({icon_name.red()}, {icon_name.green()}, {icon_name.blue()}); border-radius: 3px;")
            return _lb




    def run(self):
        """
        入口
        :return:
        """

    @_write_in
    def _add_time_row(self):
        """
        添加时间轴
        :return:
        """

    @staticmethod
    def _clear():
        """
        清除所有控件
        :return:
        """
        if isinstance(frames, Iterable):
            for frame in frames:
                if hasattr(frame, 'deleteLater'):
                    frame.deleteLater()
                    frame.setVisible(False)
                elif hasattr(frame, 'setVisible'):
                    frame.setVisible(False)

    @staticmethod
    def _get_x(msec):
        """
        将毫秒数转化为横坐标值
        :param msec:
        :return:
        """
        # 1000ms -> 40pixel
        # 25ms -> 1pixel
        _pixel = msec // 25
        return _pixel

    @_write_in
    def _add_player_skill(self, msec):
        """
        向图片中添加玩家技能
        :param msec:
        :return:
        """

        y = self._get_x(msec)























