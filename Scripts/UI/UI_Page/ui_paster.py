# coding: utf-8
# author: LinXin
# 复盘图片制作

from PyQt5.QtWidgets import QLabel, QFrame, QGroupBox, QScrollArea, QMainWindow
from PyQt5.Qt import QColor, QSize
from PyQt5.QtCore import QPoint
from PIL import Image
from collections import namedtuple
from typing import Literal, Iterable

from Scripts.UI.UI_Base.ui_other import buff_icons, skill_icons, buff_to_name
from Scripts.UI.UI_Base.ui import Ui_MainWindow

position = namedtuple('position', ['x', 'y'])
size = namedtuple('size', ['w', 'h'])
row = namedtuple('row_data', ['name', 'top_y', 'height'])

# 一次绘图中添加的所有frames
frames = None

LEFT_BORDER = 30

try:
    orange_border = Image.open(rf'Sources/Jx3_Datas/Icons/jx3basic_icons/orange.png')
except FileNotFoundError:
    orange_border = Image.new('RGBA', (48, 48), (255, 255, 255, 255))


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

    def __init__(self, parent: QMainWindow):
        self.ui: Ui_MainWindow = parent.ui
        self.widget = parent
        self._parent = self.ui.scrollAreaWidgetContents
        # 基础控件
        self._rows = {}
        self._lines = None
        self._figure = self._set_figure()
        self._set_rows()
        # 战斗时间
        self._fight_time = 0
        # 战斗记录
        self._skill_data = None

        self.ui.scrollArea.wheelEvent = self._scroll_event

    def _scroll_event(self, a0):
        horizontal_bar = self.ui.scrollArea.horizontalScrollBar()
        delta_x = -a0.angleDelta().y()  # 鼠标只能纵向滚动
        v = horizontal_bar.value() + delta_x
        v = max(min(v, horizontal_bar.maximum()), horizontal_bar.minimum())  # 限制横向滚动条的value值。
        horizontal_bar.setValue(v)  # 设置滚动值

    def _set_figure(self):
        """
        初始化时生成图例
        :return:
        """
        _fig = QGroupBox(self.ui.scrollArea)
        _fig.resize(30, self._parent.height())
        _fig.move(0, 0)
        _fig.setStyleSheet("border: 1px solid rgb(0, 0, 0); border-radius: 0px;")
        return _fig

    def _set_rows(self):
        """
        初始化时生成每一行的GroupBox和分界线
        :return:
        """
        ROWS = {
            0: row('时间轴', 130, 15),
            1: row('非gcd技能轴', 145, 20),
            2: row('gcd技能轴', 165, 25),
        }

        # 顶线

        def get_line() -> QFrame:
            _line = QFrame(self._parent)
            _line.setFrameStyle(QFrame.HLine | QFrame.Plain)
            _line.setLineWidth(1)
            _line.resize(10, 1)
            _line.setStyleSheet("background-color: rgb(0, 0, 0);")
            _line.raise_()
            return _line

        row_tp = None
        for row_tp in ROWS.values():
            # 每行的groupbox
            _gb = QGroupBox(self._parent)
            _gb.resize(10, row_tp.height)
            _gb.move(LEFT_BORDER, row_tp.top_y)
            _gb.setStyleSheet("background-color: rgb(247, 245, 243); color: rgb(0, 0, 0);")
            _gb.setVisible(False)
            # 每行的line
            _line = get_line()
            _line.move(LEFT_BORDER, row_tp.top_y - 1)
            _line.setVisible(False)
            # 储存行
            self._rows[row_tp.name] = _gb
            # 储存分割线
            if self._lines is None:
                self._lines = [_line]
            else:
                self._lines.append(_line)
        # 最后一行行尾的线
        if row_tp is not None:
            _line = get_line()
            _line.move(LEFT_BORDER, row_tp.top_y + row_tp.height - 1)
            _line.setVisible(False)
            if self._lines is None:
                self._lines = [_line]
            else:
                self._lines.append(_line)

    def _new_icon_label(self, row_name: str, icon_name: str | QColor, *, icon_type: Literal["buff", None] = None,
                        border=None) -> Jx3Label:
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
                    img = skill_icons[icon_name]
                else:
                    img = buff_icons[icon_name]
            except KeyError:
                print(f"未查询到图标：{icon_name}.png")
                _lb.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 3px;")
                return _lb
            else:
                img = img.resize((_h, _h))
                if border == 'orange':
                    _border = orange_border.resize((_h, _h))
                    _, _, _, alpha = _border.split()
                    img.paste(_border, mask=alpha)
                _lb.setStyleSheet("border-radius: 3px;")
                _lb.setPixmap(img.toqpixmap())
                return _lb
        else:
            _lb.setStyleSheet(
                f"background-color: rgb({icon_name.red()}, {icon_name.green()}, {icon_name.blue()}); border-radius: 3px;")
            return _lb

    def run(self, data):
        """
        入口
        :param:
        :return:
        """
        self._fight_time, self._skill_data = data
        # 计算所需宽度
        x_pixels = self._get_x(self._fight_time) + 100
        # 修改画布宽度
        self.ui.scrollAreaWidgetContents.setMinimumWidth(x_pixels)
        # 修改行宽
        for frame in list(self._rows.values()) + self._lines:
            frame.resize(x_pixels, frame.height())
            frame.setVisible(True)
        # 开始绘图
        # 添加时间轴
        self._add_time_row()
        # 添加技能轴
        self._add_player_skill()

    @_write_in
    def _add_time_row(self):
        """
        添加时间轴
        :return:
        """
        # 10s -> 400pixels
        _ret_lbs = []
        if self._fight_time > 0:
            # 每十秒为一个刻度
            # 预留一秒
            for pos_x in range(50, self._fight_time // 25, 400):
                # 计算时间字符串
                mm, ss = divmod((pos_x - 50) / 400, 6)
                _time = f"{int(mm):02}:{int(ss * 10):02}"
                # 生成对应label
                try:
                    _parent = self._rows['时间轴']
                    _label = Jx3Label(_parent)
                except KeyError as e:
                    print(f"KeyError: {e} at Scripts/UI/UI_Page/ui_paster.py _add_time_row: 未知问题")
                else:
                    _label.setText(_time)
                    _label.resize(60, _parent.height())
                    _label.move(pos_x)
                    _ret_lbs.append(_label)
        return _ret_lbs

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
    def _add_player_skill(self):
        """
        向图片中添加玩家技能
        :return:
        """
        majors = {'盾刀', '盾击', '盾压', '盾猛', '斩刀', '闪刀', '绝刀', '劫刀', '撼地', '盾舞', '盾墙', '盾壁', '盾毅',
                  '阵云结晦', '月照连营', '雁门迢递', '断马摧城', '扬旌沙场', '矢尽兵穷', '盾反', '盾抛', '蹑云逐月', '迎风回浪',
                  '凌霄揽胜', '瑶台枕鹤'}
        _labels = []
        assert self._skill_data is not None
        for msec, skill_data in self._skill_data.items():
            _name = skill_data['name']
            _buffs = skill_data['buffs']
            # 先生成MouseHoverText
            _hover_text = ""
            if _buffs is not None:
                for buff, state in _buffs.items():
                    if buff not in buff_to_name:
                        continue
                    if state:
                        if state is True:
                            state = 1
                        _hover_text += f"{buff_to_name[buff]}:{state}\n"
            # 添加边框
            if _name in majors:
                # 小轻功不加边框
                if _name not in {'蹑云逐月', '迎风回浪', '凌霄揽胜', '瑶台枕鹤'}:
                    _label = self._new_icon_label('gcd技能轴', _name, border='orange')
                else:
                    _label = self._new_icon_label('gcd技能轴', _name)
                _label.move(self._get_x(msec))
                _labels.append(_label)
            else:
                # 后撤不加边框
                if _name not in {'后撤'}:
                    _label = self._new_icon_label('非gcd技能轴', _name, border='orange')
                else:
                    _label = self._new_icon_label('非gcd技能轴', _name)
                _label.move(self._get_x(msec))
                _labels.append(_label)
            # 添加悬浮提示
            # 删除最后一个换行符
            _label.setToolTip(_hover_text[:-1])

        return _labels
