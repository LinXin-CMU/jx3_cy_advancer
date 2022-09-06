# coding: utf-8
# author: LinXin
# 复盘图片制作

from PyQt5.QtWidgets import QLabel, QFrame, QGroupBox, QScrollArea, QMainWindow, QScrollBar, QPlainTextEdit
from PyQt5.Qt import QColor, QSize
from PyQt5.QtCore import QPoint, Qt, QEvent
from PIL import Image
from collections import namedtuple
from typing import Literal, Iterable

from Scripts.UI.UI_Base.ui_other import buff_icons, skill_icons, buff_to_name, school_colors
from Scripts.UI.UI_Base.ui import Ui_MainWindow

position = namedtuple('position', ['x', 'y'])
size = namedtuple('size', ['w', 'h'])
row = namedtuple('row_data', ['name', 'height'])

# 一次绘图中添加的所有frames
frames = None

LEFT_BORDER = 0

try:
    orange_border = Image.open(rf'Sources/Jx3_Datas/Icons/jx3basic_icons/orange.png')
except FileNotFoundError:
    orange_border = Image.new('RGBA', (48, 48), (255, 255, 255, 255))

# buff数据
_self_buff_imports = {'恋战': 9, '寒甲': 6, '坚铁': 10, '盾挡': 7, '分野': 2, '军啸': 3, '伤腰': 4, '单刀赴会·战': 11, '玉简·分山劲': 1, '残卷·铁骨衣': 8, "锋凌横绝五阵": 5}
_self_buff_to_name = {'恋战': "LianZhan", '寒甲': "HanJia", '坚铁': "JianTie", '盾挡': "DunDang", '分野': "FenYe",
                      '军啸': "JunXiao", '伤腰': "Enchant_Belt", '单刀赴会·战': "DanDao", '玉简·分山劲': "YuJian",
                      '残卷·铁骨衣': "CanJuan", '锋凌横绝五阵': "FengLing"}
_other_buff_imports = {
    "潮生": "JiangHu",
    "卫公折冲五阵": "TianCe", "激雷": "TianCe", "号令三军": "TianCe", "化干戈": "TianCe",
    "碎星辰": "ChunYang", "行天道": "ChunYang", "北斗七星五阵": "ChunYang",
    "左旋右转": "QiXiu", "泠风解怀": "QiXiu", "穿林": "QiXiu", "傲雪暗香": "QiXiu",
    "弘法": "ShaoLin",
    "梅隐香": "CangJian", "剑锋百锻": "CangJian",
    "酣畅淋漓": "GaiBang", "降龙伏虎五阵": "GaiBang",
    "朝圣言": "MingJiao",
    "圣蝎附体": "WuDu",
    "流星赶月五阵": "TangMen", "千机百变五阵": "TangMen",
    "振奋": "CangYun", "寒啸千军": "CangYun",
    "梅花三弄": "ChangGe", "弄梅": "ChangGe", "绕梁": "ChangGe", "烈雷": "ChangGe", "悲歌": "ChangGe",
    "霜岚洗锋五阵": "BaDao", "疏狂": "BaDao",
    "龙皇雪风五阵": "LingXue",
    "祝由·水坎": "YanTian", "九星游年五阵": "YanTian",
    "香稠": "YaoZong", "配伍": "YaoZong", "飘黄": "YaoZong"
}
_other_buff_to_group = {
    "潮生": 25,
    "卫公折冲五阵": 6, "激雷": 5, "号令三军": 4, "化干戈": 4,
    "碎星辰": 12, "行天道": 12, "北斗七星五阵": 13,
    "左旋右转": 21, "泠风解怀": 22, "穿林": 22, "傲雪暗香": 22,
    "弘法": 3,
    "梅隐香": 14, "剑锋百锻": 14,
    "酣畅淋漓": 16, "降龙伏虎五阵": 17,
    "朝圣言": 7,
    "圣蝎附体": 24,
    "流星赶月五阵": 15, "千机百变五阵": 15,
    "振奋": 1, "寒啸千军": 2,
    "梅花三弄": 8, "弄梅": 8, "绕梁": 8, "烈雷": 9, "悲歌": 9,
    "霜岚洗锋五阵": 18, "疏狂": 19,
    "龙皇雪风五阵": 20,
    "祝由·水坎": 23, "九星游年五阵": 23,
    "香稠": 11, "配伍": 11, "飘黄": 10
}


class ToolTipOutLabel(QLabel):
    # 自定义一个QLabel, 重写鼠标进入离开方法
    def __init__(self, tip_parent: QPlainTextEdit, *args, **kwargs):
        super(ToolTipOutLabel, self).__init__(*args, **kwargs)
        self._tip_text: str | None = None
        self._tool_tip_parent: QPlainTextEdit = tip_parent
        self._tool_tip_parent_size: size | None = None
        self._bias = _bias = position(5, 5)

    def setToolTip(self, a0: str) -> None:
        self._tip_text: str = a0
        _txt_info = self._tip_text.split('\n')
        self._tool_tip_parent_size = size(max([len(i) for i in _txt_info]) * 13, len(_txt_info) * 15 + 5)

    def enterEvent(self, a0: QEvent) -> None:
        self._tool_tip_parent.setVisible(True)
        if self._tip_text is not None:
            self._tool_tip_parent.setPlainText(self._tip_text)
            _x = self.mapFromGlobal(self.cursor().pos()).x() + self.x() + self.parent().x() + self.parent().parent().x() + self.parent().parent().parent().parent().x()
            _y = self.mapFromGlobal(self.cursor().pos()).y() + self.y() + self.parent().y() + self.parent().parent().y() + self.parent().parent().parent().parent().y()
            # 偏移几个像素
            if self.parent().parent().parent().parent().parent().width() - _x < self._tool_tip_parent.width() + 50:
                # 设置标签位于鼠标左方
                _x = _x - self._tool_tip_parent.width() - self._bias.x
            else:
                _x += self._bias.x

            if self.parent().parent().parent().parent().parent().height() - _y < self._tool_tip_parent.height() + 50:
                # 设置标签位于鼠标上方
                _y = _y - self._tool_tip_parent.height() - self._bias.y
            else:
                _y += self._bias.y
            self._tool_tip_parent.move(_x, _y)
            self._tool_tip_parent.resize(*self._tool_tip_parent_size)
        super(ToolTipOutLabel, self).enterEvent(a0)
    
    def leaveEvent(self, a0: QEvent) -> None:
        self._tool_tip_parent.setVisible(False)
        super(ToolTipOutLabel, self).leaveEvent(a0)


class Jx3Label(ToolTipOutLabel):
    # 再自定义一个QLabel, 重写move方法
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
        # buff记录
        self._benefit_buffs = None
        # 额外buff图标储存
        self._other_buff_icons = {}
        # 绑定滚轮
        self.ui.scrollArea.wheelEvent = self._scroll_event
        self.ui.scrollArea.verticalScrollBar().valueChanged.connect(self._set_figure_scroll_bar)
        # 隐藏信息提示框
        self.ui.tooltip_textEdit.setVisible(False)

    def _get_icon(self, buff_name) -> Image.Image:
        """
        获取buff图标
        :param buff_name:
        :return:
        """
        if buff_name in self._other_buff_icons:
            return self._other_buff_icons[buff_name]
        else:
            try:
                img = Image.open(rf'Sources/Jx3_Datas/Icons/buff_icons/{buff_name}.png', 'r')
                self._other_buff_icons[buff_name] = img
                return img
            except FileNotFoundError:
                return Image.open(r'Sources/Jx3_Datas/Icons/talent_icons/empty.png', 'r')


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
        # self._fig = QGroupBox(self.ui.scrollArea)
        self._fig = self.ui.scrollAreaWidgetContents_3
        self._fig.resize(30, self._parent.height())
        self._fig.move(0, 0)
        self._fig.setStyleSheet("border: 1px solid rgb(0, 0, 0); border-radius: 0px;")
        # self.ui.scrollArea_2.setVerticalScrollBar(self.ui.scrollArea.verticalScrollBar())
        self.ui.scrollArea_2.horizontalScrollBar().setVisible(False)

        return self._fig

    def _set_figure_scroll_bar(self):
        """
        图例滚动条的槽函数
        :return:
        """
        self.ui.scrollArea_2.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().value())

    def _set_rows(self):
        """
        初始化时生成每一行的GroupBox和分界线
        :return:
        """
        start = 130
        ROWS = {
            0: row('时间轴', 15),
            1: row('非gcd技能轴', 20),
            2: row('gcd技能轴', 25),
        }

        # 顶线

        def get_line() -> QFrame:
            _line = QFrame(self._parent)
            _line.setFrameStyle(QFrame.HLine | QFrame.Plain)
            _line.setLineWidth(1)
            _line.resize(10, 1)
            _line.setStyleSheet("background-color: rgba(80, 80, 80, 80);")
            _line.raise_()
            return _line

        row_tp = None
        row_y = start
        for row_tp in ROWS.values():
            # 每行的groupbox
            _gb = QGroupBox(self._parent)
            _gb.resize(10, row_tp.height)
            _gb.move(LEFT_BORDER, row_y)
            _gb.setStyleSheet("background-color: rgb(247, 245, 243); color: rgb(0, 0, 0);")
            _gb.setVisible(False)
            # 每行的line
            _line = get_line()
            _line.move(LEFT_BORDER, row_y - 1)
            _line.setVisible(False)
            # 迭代粘贴位置
            row_y += row_tp.height
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
            _line.move(LEFT_BORDER, row_y - 1)
            _line.setVisible(False)
            if self._lines is None:
                self._lines = [_line]
            else:
                self._lines.append(_line)

    @_write_in
    def _add_row(self, row_index, row_tp: row):
        """
        在运行时添加一行的方法\n
        :param row_tuple:
        :return:
        """
        _write_in_list = []

        def get_line() -> QFrame:
            _line = QFrame(self._parent)
            _line.setFrameStyle(QFrame.HLine | QFrame.Plain)
            _line.setLineWidth(1)
            _line.resize(10, 1)
            _line.setStyleSheet("background-color: rgba(80, 80, 80, 80);")
            _line.raise_()
            return _line

        # 画布宽度
        x_pixels = self._get_x(self._fight_time) + 100
        # 画布y坐标
        # 同时检查画布是否需要扩大
        if row_index > 0:
            y_pixels = self._lines[-1].y() + 1
            if y_pixels + row_tp.height > self._parent.height():
                self._parent.setMinimumHeight(y_pixels + row_tp.height + 10)
                self._parent.resize(self._parent.width(), y_pixels + row_tp.height + 10)
                self._fig.setMinimumHeight(y_pixels + row_tp.height + 30)
                self._fig.resize(self._fig.width(), y_pixels + row_tp.height + 30)
        else:
            y_pixels = self._lines[1].y() - row_tp.height
            if y_pixels < 0:
                self._parent.setMinimumHeight(self._parent.height() + abs(y_pixels) + 10)
                self._parent.resize(self._parent.width(), self._parent.height() + abs(y_pixels) + 10)
                self._fig.setMinimumHeight(self._parent.height() + abs(y_pixels) + 30)
                self._fig.resize(self._fig.width(), self._parent.height() + abs(y_pixels) + 30)
                y_pixels = 10
        # 每行的groupbox
        _gb = QGroupBox(self._parent)
        _gb.resize(10, row_tp.height)
        _gb.move(LEFT_BORDER, y_pixels)
        _gb.resize(x_pixels, row_tp.height)
        _gb.setStyleSheet("background-color: rgb(247, 245, 243); color: rgb(0, 0, 0);")
        # 每行的line
        _line = get_line()
        _line.resize(x_pixels, 1)
        # 判断添加到下方还是上方
        if row_index > 0:
            # 下方
            _line.move(LEFT_BORDER, y_pixels + row_tp.height - 1)
        else:
            # 上方
            _line.move(LEFT_BORDER, y_pixels - 1)

        # 储存行
        self._rows[row_tp.name] = _gb
        _write_in_list.append(_gb)
        # 储存分割线
        if self._lines is None:
            self._lines = [_line]
        else:
            self._lines.append(_line)
        _write_in_list.append(_line)
        return _write_in_list

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

        _lb = Jx3Label(self.ui.tooltip_textEdit, _parent)
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

    def run(self, data, record_info):
        """
        入口
        :param:
        :return:
        """
        # 拆包数据
        self._fight_time, self._skill_data, self._benefit_buffs = data
        # 清除上一次的控件
        self._clear()
        # 计算所需宽度
        x_pixels = self._get_x(self._fight_time) + 100
        # 修改画布宽度和设置画布默认高度
        self._parent.setMinimumWidth(x_pixels)
        self._parent.setMinimumHeight(371)
        self._parent.resize(x_pixels, 371)
        self._fig.setMinimumHeight(351)
        self._fig.resize(30, 351)
        # 修改行宽
        for frame in list(self._rows.values()) + self._lines:
            frame.resize(x_pixels, frame.height())
            frame.setVisible(True)
        # 开始绘图
        # 添加时间轴
        self._add_time_row()
        # 添加技能轴
        self._add_player_skill()
        # 添加buff
        self._add_player_buff(record_info)
        # 添加刻度
        self._add_scale()


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
                    _label = Jx3Label(self.ui.tooltip_textEdit, _parent)
                except KeyError as e:
                    print(f"KeyError: {e} at Scripts/UI/UI_Page/ui_paster.py _add_time_row: 未知问题")
                else:
                    _label.setText(_time)
                    _label.resize(60, _parent.height())
                    _label.move(pos_x - 17)
                    _ret_lbs.append(_label)
        return _ret_lbs

    def _clear(self):
        """
        清除所有控件
        :return:
        """
        global frames
        if isinstance(frames, Iterable):
            # 删除self._rows中的frame
            _del = []
            for k, v in self._rows.items():
                if v in frames:
                    _del.append(k)
            for k in _del:
                del self._rows[k]
            # 删除self._lines中的frame
            if isinstance(self._lines, list):
                for item in reversed(self._lines):
                    if item in frames:
                        self._lines.remove(item)

            for frame in frames:
                if hasattr(frame, 'deleteLater'):
                    frame.deleteLater()
                    frame.setVisible(False)
                elif hasattr(frame, 'setVisible'):
                    frame.setVisible(False)
            frames = None


    @staticmethod
    def _get_x(msec, *, position=False):
        """
        将毫秒数转化为横坐标值
        :param msec:
        :return:
        """
        # 1000ms -> 40pixel
        # 25ms -> 1pixel
        _pixel = msec // 25
        if position:
            _pixel += 50
        return _pixel

    @_write_in
    def _add_player_skill(self):
        """
        向图片中添加玩家技能\n
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
                _label.move(self._get_x(msec, position=True))
                _labels.append(_label)
            else:
                # 后撤不加边框
                if _name not in {'后撤'}:
                    _label = self._new_icon_label('非gcd技能轴', _name, border='orange')
                else:
                    _label = self._new_icon_label('非gcd技能轴', _name)
                _label.move(self._get_x(msec, position=True))
                _labels.append(_label)
            # 添加悬浮提示
            # 删除最后一个换行符
            _label.setToolTip(_hover_text[:-1])

        return _labels

    @_write_in
    def _add_player_buff(self, record_info):
        """
        向图片中添加自身buff
        :param record_info:
        :return:
        """
        # 玩家角色名信息
        _player_names = record_info['name_data']
        # 返回值
        _ret_frames = []
        # 先过滤需要展示的自身buff
        _self_buffs = {}
        for buff_id, buff_data in self._benefit_buffs[1].items():
            buff_name = buff_data['name']
            if buff_name in _self_buff_imports and buff_id not in {'8271_1'}:
                # 特殊筛选: 过滤小寒甲
                if buff_name not in _self_buffs:
                    _self_buffs[buff_name] = buff_data['times']
                else:
                    _self_buffs[buff_name] += buff_data['times']
        # 根据数量生成自身buff行
        self._add_row(3, row('自身buff', len(_self_buffs) * 15))
        # 生成buff持续时间线
        _self_buffs = {i: _self_buffs[i] for i in sorted(_self_buffs, key=lambda i: _self_buff_imports[i])}
        for index, buff_name in enumerate(_self_buffs.keys()):
            if index % 2 == 0:
                _color = "#FFA176"
                _font_color = "rgb(0, 0, 0)"
            else:
                _color = "#A63400"
                _font_color = "rgb(255, 255, 255)"
            for buff_data in _self_buffs[buff_name]:
                start_time, end_time, level, layer, src_player = buff_data
                # 先获取玩家角色名
                if src_player in _player_names:
                    src_player = _player_names[src_player]['szName']
                else:
                    src_player = '未知目标'
                _hover_text = f"{buff_name}:\nbuff等级:{level}\nbuff层数:{layer}\n来源:{src_player}"
                _buff_label = ToolTipOutLabel(self.ui.tooltip_textEdit, self._rows['自身buff'])
                _buff_label.resize(15, 15)
                _buff_label.setStyleSheet(f"background-color: {_color}; font-size: 9pt;")
                _buff_label.setPixmap(buff_icons[_self_buff_to_name[buff_name]].resize((15, 15)).toqpixmap())
                _buff_label.move(self._get_x(start_time, position=True), index*15)
                _buff_label.setToolTip(_hover_text)
                _buff_time_line = ToolTipOutLabel(self.ui.tooltip_textEdit, self._rows['自身buff'])
                _buff_time_line.resize(self._get_x(end_time - start_time) - 15, 15)
                _buff_time_line.setStyleSheet(f"background-color: {_color}; font-size: 8pt; color: {_font_color}")
                _buff_time_line.move(self._get_x(start_time, position=True) + 15, index*15+0)
                _buff_time_line.setText(f"×{layer}")
                _buff_time_line.setToolTip(_hover_text)
                _ret_frames += [_buff_time_line, _buff_label]
            # 生成图例
            _fig_label = ToolTipOutLabel(self.ui.tooltip_textEdit, self._fig)
            _fig_label.resize(self._fig.width(), 15)
            _fig_label.move(0, self._rows['自身buff'].y()+index*15)
            _fig_label.setStyleSheet(f"font-size: 8pt; border: none;")
            _fig_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            _fig_label.setText(buff_name[:2])
            _ret_frames.append(_fig_label)
        # 调用下方buff序列，保证颜色明暗顺序
        self._add_other_buff(_player_names)
        return _ret_frames

    @_write_in
    def _add_other_buff(self, _player_names):
        """
        向图片中添加其他增益buff
        :param record_info:
        :return:
        """
        # 返回值
        _ret_frames = []
        # 先过滤需要展示的增益buff
        _other_buffs = {}
        for buff_id, buff_data in self._benefit_buffs[0].items():
            buff_name = buff_data['name']
            if buff_name in _other_buff_imports and buff_id not in {'8271_1'}:
                # 特殊筛选: 过滤小寒甲
                if buff_name not in _other_buffs:
                    _other_buffs[buff_name] = buff_data['times']
                else:
                    _other_buffs[buff_name] += buff_data['times']
        # 根据数量生成自身buff行
        self._add_row(4, row('增益buff', len(_other_buffs) * 15))
        # 生成buff持续时间线
        _other_buffs = {k: _other_buffs[k] for k in sorted(_other_buffs.keys(), key=lambda i: _other_buff_to_group[i])}
        # 记录已存在的门派和组
        _has_groups = {}
        # 已叠加的buff, 需要在index中减去
        _index_minus = 0
        for index, buff_name in enumerate(_other_buffs.keys()):
            index -= _index_minus
            # 判断当前buff是否是新的一行buff，如不是的话不设置图例
            _need_fig = True
            # 记录buff所属的门派和行分组
            _g = _other_buff_to_group[buff_name]
            _m = _other_buff_imports[buff_name]
            if _m not in _has_groups:
                _has_groups[_m] = {'group': {_g: index}, 'count': 1}
            elif _g not in _has_groups[_m]['group']:
                _has_groups[_m]['group'][_g] = index
                _has_groups[_m]['count'] += 1
            else:
                # 修改当前index，关联buff处于哪一行
                index = _has_groups[_m]['group'][_g] - _index_minus
                _index_minus += 1
                _has_groups[_m]['count'] += 1
                # 取消图例显示
                _need_fig = False
            # 根据组别查找对应背景颜色和字体颜色
            _belong_school = _other_buff_imports[buff_name]
            if _belong_school in school_colors:
                if _has_groups[_m]['count'] % 2 == 1:
                    # bright
                    _bg_color = school_colors[_belong_school][0]
                    _color = '#000000'
                else:
                    # dark
                    _bg_color = school_colors[_belong_school][1]
                    _color = '#ffffff'
                # _bg_color = school_colors[_belong_school][0]
                # _color = '#000000'
            else:
                return
            for buff_data in _other_buffs[buff_name]:
                start_time, end_time, level, layer, src_player = buff_data
                # 先获取玩家角色名
                if src_player in _player_names:
                    src_player = _player_names[src_player]['szName']
                else:
                    src_player = '未知目标'
                _hover_text = f"{buff_name}:\nbuff等级:{level}\nbuff层数:{layer}\n来源:{src_player}"
                _buff_label = ToolTipOutLabel(self.ui.tooltip_textEdit, self._rows['增益buff'])
                _buff_label.resize(15, 15)
                _buff_label.setStyleSheet(f"background-color: {_bg_color}; font-size: 9pt;")
                _buff_label.setPixmap(self._get_icon(buff_name).resize((15, 15)).toqpixmap())
                _buff_label.move(self._get_x(start_time, position=True), index * 15)
                _buff_label.setToolTip(_hover_text)
                _buff_time_line = ToolTipOutLabel(self.ui.tooltip_textEdit, self._rows['增益buff'])
                _buff_time_line.resize(self._get_x(end_time - start_time) - 15, 15)
                _buff_time_line.setStyleSheet(f"background-color: {_bg_color}; font-size: 8pt; color: {_color}")
                _buff_time_line.move(self._get_x(start_time, position=True) + 15, index * 15 + 0)
                _buff_time_line.setText(f"×{layer}")
                _buff_time_line.setToolTip(_hover_text)
                _ret_frames += [_buff_time_line, _buff_label]
            # 生成图例
            if _need_fig:
                _fig_label = ToolTipOutLabel(self.ui.tooltip_textEdit, self._fig)
                _fig_label.resize(self._fig.width(), 15)
                _fig_label.move(0, self._rows['增益buff'].y() + index * 15)
                _fig_label.setStyleSheet(f"font-size: 8pt; border: none;")
                _fig_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                _fig_label.setText(buff_name[:2])
                _ret_frames.append(_fig_label)

        return _ret_frames

    @_write_in
    def _add_scale(self):
        """
        添加刻度
        :return:
        """
        _lines = []
        line_height = self._parent.height()
        for pos_x in range(50, self._fight_time // 25, 200):
            _line = QFrame(self._parent)
            _line.setFrameStyle(QFrame.HLine | QFrame.Plain)
            _line.setLineWidth(1)
            _line.resize(1, line_height)
            _line.move(pos_x, 0)
            _line.setStyleSheet("background-color: rgba(80, 80, 80, 80);")
            _line.raise_()
            _lines.append(_line)
        return _lines





