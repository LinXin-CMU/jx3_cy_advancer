# coding: utf-8
# author: LinXin
"""
计算器页面的相关操作
"""

from PyQt5.QtWidgets import QMainWindow, QLabel, QInputDialog, QLineEdit
from win32clipboard import OpenClipboard, CloseClipboard, SetClipboardText, EmptyClipboard

from Scripts.UI.UI_Base.ui_base import BaseUi
from Scripts.UI.UI_Base.ui import Ui_MainWindow
from CustomClasses.TypeHints import Attribute


class Calculator_UI(BaseUi):

    def __init__(self, obj: QMainWindow):
        super().__init__()
        self.ui: Ui_MainWindow = obj.ui
        self.widget = obj
        # print(f"class Calculator_UI: {id(self.ui)}")
        # 装备label已在designer中生成过了, 这里不涉及重复生成的问题
        self._attribute_labels = None
        # 储存显示属性所用的label，便于修改
        self._talent_labels = None
        # 储存显示奇穴所用的label，便于修改
        self._json_attribute = None

        # 绑定按钮
        self.ui.export_json_button.clicked.connect(self._show_json_widget)

    def show_labels(self, attribute: Attribute):
        """
        用于装备、属性和奇穴的展示\n
        :param attribute:
        :return:
        """
        self._json_attribute = attribute.json_attributes
        self._set_equip_label()
        self._set_attribute_label(attribute)
        self._set_talent_label(attribute)


    def _set_equip_label(self):
        """
        将装备信息设置到计算器页面的详细装备信息中
        """
        label_dict = {
            'HAT': 'hat',
            'JACKET': 'jacket',
            'BELT': 'belt',
            'WRIST': 'wrist',
            'BOTTOMS': 'bottoms',
            'SHOES': 'shoes',
            'NECKLACE': 'necklace',
            'PENDANT': 'pendant',
            'RING_1': 'ring1',
            'RING_2': 'ring2',
            'PRIMARY_WEAPON': 'weapon',
            'SECONDARY_WEAPON': 'secweap',
        }
        for equip_key in self.equip:
            # 过滤掉该部位未穿装备的情况
            if self.equip[equip_key] is None:
                continue
            # 装备名称栏
            if hasattr(self.ui, f'equip_{label_dict[equip_key]}_name'):
                label = getattr(self.ui, f'equip_{label_dict[equip_key]}_name')
                label.setText(f"{self.equip[equip_key].name}-{str(self.equip[equip_key].level)}")
            # 小附魔栏
            if hasattr(self.ui, f'equip_{label_dict[equip_key]}_enchance'):
                label = getattr(self.ui, f'equip_{label_dict[equip_key]}_enchance')
                label.setText(f'{self.equip[equip_key].enhance}')
                label.setStyleSheet('QLabel{font-size:9pt;}')
            # 大附魔栏
            if hasattr(self.ui, f'equip_{label_dict[equip_key]}_enchant'):
                label = getattr(self.ui, f'equip_{label_dict[equip_key]}_enchant')
                label.setText(f'{self.equip[equip_key].enchant}')
                label.setStyleSheet('QLabel{font-size:9pt;}')
            # 五彩石栏
            if equip_key == 'PRIMARY_WEAPON':
                self.ui.equip_weapon_stone.setText(self.equip[equip_key].stone['name'])

    def _set_attribute_label(self, attribute: Attribute):
        """
        用于展示玩家属性\n
        :param attribute:
        :return:
        """
        attributes = [
            "Agility", "PhysicsAttackPower", "PhysicsCriticalStrikeRate", "PhysicsCriticalDamagePowerPercent",
            "PhysicsOvercomePercent", "StrainPercent", "SurplusValue", "HastePercent", "Vitality", "PhysicsShieldPercent",
            "LunarShieldPercent", "ToughnessDefCriticalPercent", "ParryPercent", "ParryValue", "DodgePercent"
        ]
        # 生成一个共享的迭代器
        # _iter = iter(attributes)
        # 转换为dict
        json_attribute = eval(attribute.json_attributes)
        # 1. 在指定坐标生成QLabel
        attack_y_range = range(66, 290, 30)
        defense_y_range = range(330, 511, 30)
        x_pos = 450
        for index, y in enumerate(attack_y_range):
            # 这两种是第一次加载时的情况
            if self._attribute_labels is None:
                label = QLabel(self.ui.groupBox_13)
                self._attribute_labels = [label]
                label.move(x_pos, y)
                label.resize(120, 16)
                label.setStyleSheet("QLabel{color: rgb(236, 99, 65);}")
            elif len(self._attribute_labels) < 15:
                label = QLabel(self.ui.groupBox_13)
                self._attribute_labels.append(label)
                label.move(x_pos, y)
                label.resize(120, 16)
                label.setStyleSheet("QLabel{color: rgb(236, 99, 65);}")
            # 这种是已经生成过label的情况
            else:
                label = self._attribute_labels[index]

        # 2. 读取并填写对应数据
            _value = json_attribute[attributes[index]]
            # 数据格式化输出
            if isinstance(_value, int):
                _text = repr(_value)
            else:
                _text = f"{_value:.2%}"
            if index == 1:
                # 攻击
                _text += f"({json_attribute['PhysicsAttackPowerBase']})"
            elif index == 7:
                # 加速
                if _text == '0':
                    _text = '0.00%'
                _text += f"({attribute['atHasteBase']})"
            label.setText(_text)

        for index, y in enumerate(defense_y_range):
            # 这两种是第一次加载时的情况
            if self._attribute_labels is None:
                label = QLabel(self.ui.groupBox_13)
                self._attribute_labels = [label]
                label.move(x_pos, y)
                label.resize(120, 16)
                label.setStyleSheet("QLabel{color: rgb(236, 99, 65);}")
            elif len(self._attribute_labels) < 15:
                label = QLabel(self.ui.groupBox_13)
                self._attribute_labels.append(label)
                label.move(x_pos, y)
                label.resize(120, 16)
                label.setStyleSheet("QLabel{color: rgb(236, 99, 65);}")
            # 这种是已经生成过label的情况
            else:
                label = self._attribute_labels[index + 8]

            _value = json_attribute[attributes[index+8]]
            if isinstance(_value, int):
                _text = repr(_value)
            else:
                _text = f"{_value:.2%}"
            if index == 4:
                # 招架
                _text += f"({attribute['atParryBase']})"
            label.setText(_text)

    def _set_talent_label(self, attribute: Attribute):
        """
        展示奇穴\n
        :param attribute:
        :return:
        """
        y_range = range(66, 397, 30)
        x_pos = 620
        for index, talent in enumerate(attribute.player_talent):
            # 这两种是第一次加载时的情况
            if self._talent_labels is None:
                label = QLabel(self.ui.groupBox_13)
                self._talent_labels = [label]
                label.move(x_pos, y_range[index])
                label.resize(120, 16)
                label.setStyleSheet("QLabel{color: rgb(236, 99, 65);}")
            elif len(self._talent_labels) < 12:
                label = QLabel(self.ui.groupBox_13)
                self._talent_labels.append(label)
                label.move(x_pos, y_range[index])
                label.resize(120, 16)
                label.setStyleSheet("QLabel{color: rgb(236, 99, 65);}")
            # 这种是已经生成过label的情况
            else:
                label = self._talent_labels[index]
            label.setText(talent)

    def _show_json_widget(self):
        """
        显示json属性的小窗口\n
        :return:
        """
        def ok():
            OpenClipboard()
            EmptyClipboard()
            SetClipboardText(self._json_attribute)
            CloseClipboard()
            print("成功复制")

        # 未读取到装备时则不显示
        if self._json_attribute is None:
            self.ShowWarningBoxForNotStartRead(self.widget)
        else:
            json_dialog = QInputDialog(self.widget)
            json_dialog.setOkButtonText("复制")
            json_dialog.setCancelButtonText("取消")
            json_dialog.setTextValue(self._json_attribute)
            json_dialog.setWindowTitle("属性数据")
            json_dialog.setLabelText("json数据：")
            # QInputDialog.setOkButtonText("复制")
            # QInputDialog.setCancelButtonText("取消")
            # _, ok = json_dialog.getText(self.widget, "属性数据", "", QLineEdit.Normal, self._json_attribute)
            json_dialog.accepted.connect(ok)
            json_dialog.rejected.connect(json_dialog.close)
            json_dialog.show()










