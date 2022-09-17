# coding: utf-8
# author: LinXin

from PyQt5.QtWidgets import QMessageBox, QPushButton

from Scripts.Config.config import ConfigSetting
from Scripts.UI.UI_Base.ui_style import UiStyle
from CustomClasses.TypeHints import Equip


class BaseUi:
    """
    所有ui界面的基类，储存数据和警告内容
    """

    def __init__(self):
        # 不可改变大小
        # ?未知作用
        self.m_drag = False
        # config初始化
        self.config = ConfigSetting()
        # 装备数据
        self.equip: dict[str: Equip] = None

    # 警告弹窗

    @staticmethod
    def ShowWarningBoxForNoName(parent):
        QMessageBox.warning(parent, '错误!', '未填写角色名！')

    @staticmethod
    def ShowWarningBoxForNotFountJx3GameError(parent):
        QMessageBox.warning(parent, '错误!', '未能读取到剑网3游戏路径, 请手动选择!')

    @staticmethod
    def ShowWarningBoxForJx3GamePathSelectError(parent):
        QMessageBox.warning(parent, '错误!', '选择的剑网3游戏路径有误, 请重新选择!')

    @staticmethod
    def ShowWarningBoxForIdNotInGamePath(parent):
        QMessageBox.warning(parent, '错误!', '未检测到该id的jcl文件夹, 请检查id是否有误!')

    @staticmethod
    def ShowWarningBoxForNotHaveJclFolder(parent):
        QMessageBox.warning(parent, '错误!', '未检测到该id的jcl文件夹, 请检查id或游戏内设置是否有误!')

    @staticmethod
    def ShowWarningBoxForNoPath(parent):
        QMessageBox.warning(parent, '错误!', '未检测到战斗记录文件, 请重新选择!')

    @staticmethod
    def ShowWarningBoxForCantGuessName(parent):
        QMessageBox.warning(parent, '错误!', '未能从文件中自动读取到当前角色, 请手动填写角色名, 或检查文件选择是否正确!')

    @staticmethod
    def ShowWarningBoxForTooManyGuessName(parent):
        QMessageBox.warning(parent, '错误!', '这把的苍云也太多了吧, 还是自己填写吧。')

    @staticmethod
    def ShowWarningBoxForFileTooSmall(parent):
        QMessageBox.warning(parent, '警告!', '战斗数据不足60s, 仅能显示复盘！')

    @staticmethod
    def ShowWarningBoxForNotFoundPlayer(parent):
        QMessageBox.warning(parent, '错误!', '未在战斗记录中检测到当前角色, 请检查是否填写错误！')

    @staticmethod
    def ShowWarningBoxForNotSettingFightTime(parent):
        QMessageBox.warning(parent, '错误!', '战斗时间不能为零！')

    @staticmethod
    def ShowWarningBoxForNoArmorInfo(parent):
        QMessageBox.warning(parent, '错误!', '未检测到装备信息，可能是复盘角色并非自身！')

    @staticmethod
    def ShowWarningBoxForNotStartRead(parent):
        QMessageBox.warning(parent, '错误!', '还没有分析文件, 无数据！')

    @staticmethod
    def ShowWarningBoxForFileEncodeError(parent):
        QMessageBox.warning(parent, '错误!', '文件编码已损坏，请选择其他文件吧！')

    @staticmethod
    def ShowInfoBoxForExportSuccess(parent, export_type):
        QMessageBox.information(parent, '操作成功!', f'{export_type}文件导出成功！')

    @staticmethod
    def ShowWarningBoxForSSLError(parent):
        QMessageBox.warning(parent, '错误!', '未能访问到jx3box服务器，请关闭本机网络代理服务(vpn)！')

    @staticmethod
    def ShowWarningBoxForPlayerKungFuWarning(parent):
        QMessageBox.warning(parent, '警告!', '当前玩家并非分山劲心法，仅能导出excel格式记录！')

    @staticmethod
    def ShowWarningBoxForMarkingError(parent):
        QMessageBox.warning(parent, '错误!', '评分模块数据异常，无法计算得分！')

    def set_equip(self, equip: dict[str: Equip]):
        """
        接入装备数据的接口\n
        :param equip:
        :return:
        """
        self.equip = equip
