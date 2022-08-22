from PyQt5.QtWidgets import QApplication, QPushButton

from Scripts.UI.ui_main import MainUi
from Scripts.UI.UI_Base.ui_other import set_page
from Scripts.ReadData.reader_main import FileReader
from Scripts.Config.config import ConfigSetting
from Scripts.JclAnalysis.analysis_main import Analysis
from CustomClasses.Exceptions import *

app = QApplication([])


class Main:

    def __init__(self):
        # 初始化config
        self.config = ConfigSetting()
        # 初始化文件读取器
        self.reader = FileReader()
        # 初始化ui界面
        self.main_ui = MainUi()
        # print(f"main.py: {id(self.main_ui.ui)}")
        # 初始化行为分析
        self.analyzer = Analysis(self.reader)
        # 绑定ui按钮
        self._button_connection()
        # 复盘用文件路径和角色名
        self._run_data = [None, None]

    def _run_reader(self):
        """
        用于执行读取文件及ui展示的入口函数\n
        :return:
        """
        try:
            self.reader.run(*self.main_ui.page_top.run_data)
            # 读取文件
            # 读取装备部分
            self.reader.get_equip_info()
            # 生成装备对象
            self._sub_calc_equip()
            # 计算剩余内容
            # 读取行为部分
            self.analyzer.run()
            # 设置技能统计
            self._sub_show_skills()
        except JclFileEncodeError:
            self.main_ui.ShowWarningBoxForFileEncodeError(self.main_ui)
        except NotFoundPlayerIDFromName:
            self.main_ui.ShowWarningBoxForNotFoundPlayer(self.main_ui)
        except JclFileTypeError:
            self.main_ui.ShowWarningBoxForNoPath(self.main_ui)
        except NotFoundJclFileError:
            self.main_ui.ShowWarningBoxForNoPath(self.main_ui)


    def _sub_calc_equip(self, current_index=None):
        """
        用于从精炼镶嵌计算到最终属性的全过程\n
        :return:
        """
        try:
            self.main_ui.page_equip.set_embedding_and_strength_info(equip=self.reader.equip)
            # 读取精炼镶嵌预设信息并计入
            self.reader.calc_attribute(self.main_ui.page_equip.embedding_and_strength_info, current_index)
            # 翻译装备信息和属性
            self.main_ui.set_equip(self.reader.equip)
            # 记录到各页面
            self.main_ui.page_calc.show_labels(self.reader.attribute)
            # 展示信息
        except AttributeError as e:
            print(f"AttributeError: {e} at main.py _sub_calc_equip: 过滤未读取装备时的装备栏设置页面切出情况")
        except TypeError as e:
            print(f"TypeError: {e} at main.py _sub_calc_equip: 过滤未读取装备时的装备栏设置页面切出情况")

    def _sub_show_skills(self):
        """
        用于展示战斗中的技能统计界面\n
        :return:
        """
        self.main_ui.page_retro.set_skill_data_table(self.analyzer.DATA_skill_to_table)


    def _button_connection(self):
        """
        用于绑定需要数据交换的各按钮\n
        :return:
        """
        # 主函数按钮
        self.main_ui.ui.MainButton.clicked.connect(self._run_reader)

        # 切换页面按钮
        # 从装备栏设置页面切换出页面所用
        buttons: list[QPushButton] = [self.main_ui.ui.pageButton_0, self.main_ui.ui.pageButton_1, self.main_ui.ui.pageButton_2]
        for button in buttons:
            button.clicked.connect(lambda _: self._sub_calc_equip(current_index=self.main_ui.ui.stackedWidget.currentIndex()))
        # 绑定页面切换，同时保证与上部分的先后次序
        for i in range(4):
            # 0-3
            button = getattr(self.main_ui.ui, f"pageButton_{i}")
            button.clicked.connect(set_page(i, self.main_ui.ui.stackedWidget.setCurrentIndex))
        self.main_ui.ui.EquipInfoButton.clicked.connect(lambda _: self.main_ui.ui.stackedWidget.setCurrentIndex(2))

        self.main_ui.ui.export_excel_button.clicked.connect(lambda: self.main_ui.page_top.export_csv_data(self.reader.csv_data))



if __name__ == '__main__':

    m = Main()
    m.main_ui.show()
    # print("xxx")
    # reader = JclReader()
    # print(reader.run("Sources/MY_Sources/2022-03-15-15-36-12-帮会领地-极境试炼木桩.jcl"))
    app.exec_()


