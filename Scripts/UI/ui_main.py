# coding: utf-8
# author: LinXin
"""
ui操作的上层接口
"""

from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from .UI_Page.ui_equip import Calculator_UI
from .UI_Page.ui_equip_setting import Equip_UI
from .UI_Page.ui_retro import Retro_UI
from .UI_Page.ui_top import Top_UI
from .UI_Page.ui_mark import Marker_UI
from .UI_Base.ui_base import BaseUi, UiStyle
from .UI_Base.ui import Ui_MainWindow

from CustomClasses.TypeHints import Equip


class MainUi(UiStyle, QMainWindow, BaseUi):
    """
    顶层ui类
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(r"Sources/UI_Resources/icon.ico"))
        # 页面
        self.page_equip = Equip_UI(self)
        self.page_calc = Calculator_UI(self)
        self.page_retro = Retro_UI(self)
        self.page_top = Top_UI(self)
        self.page_mark = Marker_UI(self)
        self.pages: list[BaseUi] = [self.page_calc, self.page_equip]
        # 界面样式初始化
        self._widget_init()

    def set_equip(self, equip: dict[str: Equip]):
        """
        将equip_data映射到所有页面类\n
        :param equip:
        :return:
        """
        self.equip = equip
        for page in self.pages:
            page.set_equip(self.equip)

    def _widget_init(self):
        """
        各种控件的初始状态设定\n
        :return:
        """
        # 设置页面
        self.ui.stackedWidget.setCurrentIndex(0)
        # 设置菜单栏按钮
        self.ui.minusButton.clicked.connect(self.showMinimized)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.minusButton.setIcon(QIcon(r'Sources/UI_Resources/minimumWindow.png'))
        self.ui.closeButton.setIcon(QIcon(r'Sources/UI_Resources/closeWindow.png'))
        self.ui.minusButton.setIconSize(QSize(30, 20))
        self.ui.closeButton.setIconSize(QSize(30, 20))
        # 测试用
        self.ui.top_fight_time_timeedit.timeChanged.connect(self.get_limit_time)

    def page_button_style(self, index):
        """
        选择页面按钮的样式设置
        :return:
        """
        stylesheet_inside = """
            QPushButton{
                background-color: rgb(226, 221, 215);
                color: #000000
            }
        """
        for i in range(4):
            # 0-3号pushbutton
            stylesheet_normal = """
                        QPushButton{
                            background-color: rgb(206, 81, 53);
                            color: #ffffff
                        }
                    """
            button: QPushButton = getattr(self.ui, f"pageButton_{i}")
            button.setStyleSheet(stylesheet_normal)
        button: QPushButton = getattr(self.ui, f"pageButton_{index}")
        button.setStyleSheet(stylesheet_inside)

    def get_limit_time(self) -> int:
        """
        返回战斗毫秒数
        :return:
        """
        _time = self.ui.top_fight_time_timeedit.time().toPyTime()
        ms = _time.hour * 60 * 1000 + _time.minute * 1000 + 999
        return ms