"""
用于装备设置界面相关操作
"""
from PyQt5.QtWidgets import QSpinBox, QPushButton, QInputDialog, QLineEdit, QMessageBox, QMainWindow
from typing import Literal

from Scripts.UI.UI_Base.ui_base import BaseUi
from Scripts.UI.UI_Base.ui import Ui_MainWindow
from Sources.Jx3_Datas.JclData import slot_to_name_dictionary
from CustomClasses.TypeHints import Equip


class Equip_UI(BaseUi):
    """
    装备栏界面
    """
    def __init__(self, obj: QMainWindow):
        super().__init__()
        self.ui: Ui_MainWindow = obj.ui
        self.widget = obj
        # print(f"class Equip_UI: {id(self.ui)}")
        self._combobox_items = {0: "默认配置", 1: None, 2: None, 3: None}
        # 储存combobox名称和位置
        self._combobox_reversed = {"默认配置": 0}
        # 读取combobox名称的映射
        # self._combobox_text = "默认配置"
        # # 储存当前combobox的位置，过滤后台引起的信号
        # 不需要
        self._setting_data = {
            'HAT': {'embedding': {1: {'QSpinBox': self.ui.equipsetting_hat_spinbox_1, 'value': None,
                                      'QLabel': self.ui.equipsetting_hat_label_1, 'embedding_data': None},
                                  2: {'QSpinBox': self.ui.equipsetting_hat_spinbox_2, 'value': None,
                                      'QLabel': self.ui.equipsetting_hat_label_2, 'embedding_data': None}, 3: None},
                    'strength': {'QSpinBox': self.ui.equipsetting_hat_spinbox, 'value': None}},
            'JACKET': {'embedding': {1: {'QSpinBox': self.ui.equipsetting_jacket_spinbox_1, 'value': None,
                                         'QLabel': self.ui.equipsetting_jacket_label_1, 'embedding_data': None},
                                     2: {'QSpinBox': self.ui.equipsetting_jacket_spinbox_2, 'value': None,
                                         'QLabel': self.ui.equipsetting_jacket_label_2, 'embedding_data': None},
                                     3: None},
                       'strength': {'QSpinBox': self.ui.equipsetting_jacket_spinbox, 'value': None}},
            'BELT': {'embedding': {1: {'QSpinBox': self.ui.equipsetting_belt_spinbox_1, 'value': None,
                                       'QLabel': self.ui.equipsetting_belt_label_1, 'embedding_data': None},
                                   2: {'QSpinBox': self.ui.equipsetting_belt_spinbox_2, 'value': None,
                                       'QLabel': self.ui.equipsetting_belt_label_2, 'embedding_data': None}, 3: None},
                     'strength': {'QSpinBox': self.ui.equipsetting_belt_spinbox, 'value': None}},
            'WRIST': {'embedding': {1: {'QSpinBox': self.ui.equipsetting_wrist_spinbox_1, 'value': None,
                                        'QLabel': self.ui.equipsetting_wrist_label_1, 'embedding_data': None},
                                    2: {'QSpinBox': self.ui.equipsetting_wrist_spinbox_2, 'value': None,
                                        'QLabel': self.ui.equipsetting_wrist_label_2, 'embedding_data': None}, 3: None},
                      'strength': {'QSpinBox': self.ui.equipsetting_wrist_spinbox, 'value': None}},
            'BOTTOMS': {'embedding': {1: {'QSpinBox': self.ui.equipsetting_bottom_spinbox_1, 'value': None,
                                          'QLabel': self.ui.equipsetting_bottom_label_1, 'embedding_data': None},
                                      2: {'QSpinBox': self.ui.equipsetting_bottom_spinbox_2, 'value': None,
                                          'QLabel': self.ui.equipsetting_bottom_label_2, 'embedding_data': None},
                                      3: None},
                        'strength': {'QSpinBox': self.ui.equipsetting_bottom_spinbox, 'value': None}},
            'SHOES': {'embedding': {1: {'QSpinBox': self.ui.equipsetting_shoes_spinbox_1, 'value': None,
                                        'QLabel': self.ui.equipsetting_shoes_label_1, 'embedding_data': None},
                                    2: {'QSpinBox': self.ui.equipsetting_shoes_spinbox_2, 'value': None,
                                        'QLabel': self.ui.equipsetting_shoes_label_2, 'embedding_data': None}, 3: None},
                      'strength': {'QSpinBox': self.ui.equipsetting_shoes_spinbox, 'value': None}},
            'NECKLACE': {'embedding': {1: {'QSpinBox': self.ui.equipsetting_necklace_spinbox_1, 'value': None,
                                           'QLabel': self.ui.equipsetting_necklace_label_1, 'embedding_data': None},
                                       2: None, 3: None},
                         'strength': {'QSpinBox': self.ui.equipsetting_necklace_spinbox, 'value': None}},
            'PENDANT': {'embedding': {1: {'QSpinBox': self.ui.equipsetting_pendant_spinbox_1, 'value': None,
                                          'QLabel': self.ui.equipsetting_pendant_label_1, 'embedding_data': None},
                                      2: None, 3: None},
                        'strength': {'QSpinBox': self.ui.equipsetting_pendant_spinbox, 'value': None}},
            'RING_1': {'embedding': {1: None, 2: None, 3: None},
                       'strength': {'QSpinBox': self.ui.equipsetting_ring_1_spinbox, 'value': None}},
            'RING_2': {'embedding': {1: None, 2: None, 3: None},
                       'strength': {'QSpinBox': self.ui.equipsetting_ring_2_spinbox, 'value': None}},
            'PRIMARY_WEAPON': {'embedding': {
                1: {'QSpinBox': self.ui.equipsetting_primary_weapon_spinbox_1, 'value': None,
                    'QLabel': self.ui.equipsetting_primary_weapon_label_1, 'embedding_data': None},
                2: {'QSpinBox': self.ui.equipsetting_primary_weapon_spinbox_2, 'value': None,
                    'QLabel': self.ui.equipsetting_primary_weapon_label_2, 'embedding_data': None},
                3: {'QSpinBox': self.ui.equipsetting_primary_weapon_spinbox_3, 'value': None,
                    'QLabel': self.ui.equipsetting_primary_weapon_label_3, 'embedding_data': None}},
                'strength': {'QSpinBox': self.ui.equipsetting_primary_weapon_spinbox, 'value': None}},
            'SECONDARY_WEAPON': {'embedding': {
                1: {'QSpinBox': self.ui.equipsetting_secondary_weapon_spinbox_1, 'value': None,
                    'QLabel': self.ui.equipsetting_secondary_weapon_label_1, 'embedding_data': None}, 2: None, 3: None},
                'strength': {'QSpinBox': self.ui.equipsetting_secondary_weapon_spinbox,
                             'value': None}},
        }

        # 开始批量绑定SpinBox
        for position in self._setting_data:
            _embedding = self._setting_data[position]['embedding']
            _strength = self._setting_data[position]['strength']
            # 绑定镶嵌
            for embedding_hole in _embedding:
                if _embedding[embedding_hole] is not None:
                    # 绑定QSpinBox
                    spinbox_obj: QSpinBox = _embedding[embedding_hole]['QSpinBox']
                    # 初始化时先设置好值
                    _embedding[embedding_hole]['value'] = spinbox_obj.value()
                    spinbox_obj.valueChanged.connect(self._spin_box_connection(position))

            # 绑定精炼
            spinbox_obj: QSpinBox = _strength['QSpinBox']
            # _strength['value'] = spinbox_obj.value()
            # 精炼更新放在激活函数内部，便于第一次读取时的数据
            spinbox_obj.valueChanged.connect(self._spin_box_connection(position))

        # 绑定一键精炼
        for level in range(4, 7):
            if hasattr(self.ui, f"strength_{level}_button"):
                button: QPushButton = getattr(self.ui, f"strength_{level}_button")
                button.clicked.connect(self._easy_button_connection("strength", level))

        # 绑定一键镶嵌
        for level in range(4, 9):
            if hasattr(self.ui, f"embedding_{level}_button"):
                button: QPushButton = getattr(self.ui, f"embedding_{level}_button")
                button.clicked.connect(self._easy_button_connection("embedding", level))

        # 绑定保存配置
        for index in range(1, 4):
            if hasattr(self.ui, f"savesetting_{index}_button"):
                button: QPushButton = getattr(self.ui, f"savesetting_{index}_button")
                button.clicked.connect(self._saving_button_connection(index))


        # 读取config中的精炼镶嵌并设置
        config_data = eval(self.config['embedding_and_strength_default'])
        if config_data is not None and isinstance(config_data, dict):
            try:
                self._set_config_embedding_and_strength(config_data)
            except Exception as e:
                print(f"Exception: {e} at Scripts/UI/ui_equip_setting.py: config.embedding_and_strength配置中出现未知错误，可忽略")

        # 读取config中的装备栏预设并设置
        self._set_save_button_from_config()

        # 读取ComboBox的改变
        self.ui.loadsetting_comboBox.currentIndexChanged.connect(self._read_saved_data)
        # self.setting_data = {
        #   position: {
        #       embedding: {
        #           'num': {QSpinBox, value, QLabel, embedding_data},
        #                  },
        #       strength: {QspinBox, value}
        #             },
        # }

    # 下面三个闭包是用于批量绑定控件时储存控件自己的参数

    def _spin_box_connection(self, position: str) -> callable:
        """
        记录当前spinbox所绑定位置的闭包
        :param position:
        :return:
        """
        self_position = position

        def _get_spin_box_value():
            """
            读取参数并设置对应value
            :return:
            """
            self.set_embedding_and_strength_info(position=self_position)

        return _get_spin_box_value

    def _easy_button_connection(self, button_type: Literal["embedding", "strength"], level: int) -> callable:
        """
        记录当前pushbutton所对应的内容和等级
        并生成对应config dict
        :param level:
        :return:
        """
        self_type = button_type
        self_level = level
        match self_type:
            case "embedding":
                value: dict = {'HAT': {'embedding': {1: self_level, 2: self_level}, 'strength': None},
                               'JACKET': {'embedding': {1: self_level, 2: self_level}, 'strength': None},
                               'BELT': {'embedding': {1: self_level, 2: self_level}, 'strength': None},
                               'WRIST': {'embedding': {1: self_level, 2: self_level}, 'strength': None},
                               'BOTTOMS': {'embedding': {1: self_level, 2: self_level}, 'strength': None},
                               'SHOES': {'embedding': {1: self_level, 2: self_level}, 'strength': None},
                               'NECKLACE': {'embedding': {1: self_level}, 'strength': None},
                               'PENDANT': {'embedding': {1: self_level}, 'strength': None},
                               'RING_1': {'embedding': {}, 'strength': None},
                               'RING_2': {'embedding': {}, 'strength': None},
                               'PRIMARY_WEAPON': {'embedding': {1: self_level, 2: self_level, 3: self_level}, 'strength': None},
                               'SECONDARY_WEAPON': {'embedding': {1: self_level}, 'strength': None}}
            case "strength":
                value: dict = {'HAT': {'embedding': {1: None, 2: None}, 'strength': self_level},
                               'JACKET': {'embedding': {1: None, 2: None}, 'strength': self_level},
                               'BELT': {'embedding': {1: None, 2: None}, 'strength': self_level},
                               'WRIST': {'embedding': {1: None, 2: None}, 'strength': self_level},
                               'BOTTOMS': {'embedding': {1: None, 2: None}, 'strength': self_level},
                               'SHOES': {'embedding': {1: None, 2: None}, 'strength': self_level},
                               'NECKLACE': {'embedding': {1: None}, 'strength': self_level},
                               'PENDANT': {'embedding': {1: None}, 'strength': self_level},
                               'RING_1': {'embedding': {}, 'strength': self_level},
                               'RING_2': {'embedding': {}, 'strength': self_level},
                               'PRIMARY_WEAPON': {'embedding': {1: None, 2: None, 3: None}, 'strength': self_level},
                               'SECONDARY_WEAPON': {'embedding': {1: None}, 'strength': self_level}}

        def _set_easy_embedding_and_strength():
            """
            按照类型设置对应的一键功能
            :return:
            """
            self._set_config_embedding_and_strength(value)

        return _set_easy_embedding_and_strength

    def _saving_button_connection(self, index) -> callable:
        """
        记录当前pushbutton的config字段
        :return:
        """
        _value_config = f"embedding_and_strength_{index}"
        _name_config = f"saving_button_{index}"

        def _saving_embedding_and_strength():
            # 1. 弹出窗口，输入名称
            # 2. 保存到config(配置项和button名称)
            # 3. 修改button名称
            # 4. 修改QComboBox列表
            choice = None
            if self.config[_name_config] is not None:
                choice = QMessageBox.question(self.widget, "警告", "这会替换已有的配置，是否要继续保存？")
            if choice != QMessageBox.No:
                item, ispressed = QInputDialog.getText(self.widget, "输入信息", "请输入配置名", QLineEdit.Normal, f"默认配置{index}")
            # item: 用户输入的名称, ispressed: 是否添加新配置
                if ispressed:
                    self.config.add_config('equip', _value_config, self.embedding_and_strength_info)
                    self.config.add_config('widget', _name_config, item)
                    button: QPushButton = getattr(self.ui, f"savesetting_{index}_button")
                    button.setText(item)
                    # 载入选择列表
                    self._combobox_items[index] = item
                    self._combobox_reversed[item] = index
                    # 记录当前QComboBox的index
                    box_index = self.ui.loadsetting_comboBox.currentIndex()
                    # 清空并重新生成QComboBox的值
                    self.ui.loadsetting_comboBox.clear()
                    self.ui.loadsetting_comboBox.addItems([i for i in self._combobox_items.values() if i is not None])
                    # 重新设置当前值, 避免保存后跳转回默认
                    self.ui.loadsetting_comboBox.setCurrentIndex(box_index)
        return _saving_embedding_and_strength

    def _read_saved_data(self):
        """
        combobox的绑定函数，用于读取对应数据
        :return:
        """
        box = self.ui.loadsetting_comboBox
        name = box.currentText()
        # if name != self._combobox_text:
        try:
            index = self._combobox_reversed[name]
        except KeyError as e:
            print(f"KeyError: {e} at Scripts/UI/ui_equip_setting.py _set_saving_data: 过滤combobox被异常信号激活的问题")
        else:
            if index == 0:
                self._set_config_embedding_and_strength(eval(self.config['embedding_and_strength_default']))
            else:
                self._set_config_embedding_and_strength(eval(self.config[f'embedding_and_strength_{index}']))
            # self._combobox_text = name


    @property
    def embedding_and_strength_info(self):
        _ret = {}
        for equip_name in self._setting_data:
            # 精炼
            _ret[equip_name] = {'embedding': {}, 'strength': None}
            _embedding = self._setting_data[equip_name]['embedding']
            for i in _embedding:
                if _embedding[i] is not None:
                    _ret[equip_name]['embedding'][i] = _embedding[i]['value']
            # 镶嵌
            _ret[equip_name]['strength'] = self._setting_data[equip_name]['strength']['value']
        return _ret

    def _set_config_embedding_and_strength(self, value: dict):
        """
        初始化时进行config中精炼镶嵌默认数据的设置,
        进行一键精炼镶嵌/读取默认配置的设置
        :param value:
        :return:
        """
        for equip_name in value:
            # 精炼
            _embedding = value[equip_name]['embedding']
            for i in _embedding:
                if _embedding[i] is not None:
                    tar_path = self._setting_data[equip_name]['embedding'][i]
                    tar_path['value'] = _embedding[i]
                    # tar_path['QSpinBox']: QSpinBox
                    tar_path['QSpinBox'].setValue(_embedding[i])
            # 镶嵌
            _strength_value = value[equip_name]['strength']
            if _strength_value is not None:
                self._setting_data[equip_name]['strength']['QSpinBox'].setValue(_strength_value)
                self._setting_data[equip_name]['strength']['value'] = _strength_value

    def set_embedding_and_strength_info(self, equip=None, *, position=None):
        """
        用于设置镶嵌孔位的具体信息, 同时会影响equip_object的具体信息
        :param position:
        :return:
        """
        # 未读取装备时的检测
        self.equip = equip
        # 过滤掉该部位未穿装备的情况
        if self.equip is None:
            return
        # 对于每件装备
        for equip_name, equip_obj in self.equip.items():
            if equip_obj is None:
                continue
            equip_obj: Equip
            # 先取出对应孔位
            if position is not None:
                # 如果存在position， 则判断其位置
                # 用于减少改变五行石镶嵌时的运算量
                if not equip_name == position:
                    continue
            # 遍历孔位计算镶嵌
            for i in range(1, 4):
                diamond_attr = equip_obj.equip_data[f"_DiamondAttributeID{i}"]
                if self._setting_data[equip_name]['embedding'][i] is not None:
                    # 记录对应镶嵌孔属性
                    if self._setting_data[equip_name]['embedding'][i]['embedding_data'] is None:
                        self._setting_data[equip_name]['embedding'][i]['embedding_data'] = diamond_attr
                    # 读取当前SpinBox的镶嵌值
                    self._setting_data[equip_name]['embedding'][i]['value'] = \
                        self._setting_data[equip_name]['embedding'][i]['QSpinBox'].value()
                # 取出对应名称
                if diamond_attr is not None:
                    try:
                        diamond_name = slot_to_name_dictionary[diamond_attr[0]]
                    except KeyError as e:
                        print(f"KeyError: {e} at Scripts/UI/ui_equip_setting.py: 未能查询到对应属性名")
                        diamond_name = "未知属性"
                    # 生成镶嵌孔位描述信息
                    # 计算属性值
                    plug = [0, 0.195, 0.39, 0.585, 0.78, 0.975, 1.17, 1.755, 2.6]
                    value = int(max(int(diamond_attr[1]), int(diamond_attr[2])) * plug[
                        self._setting_data[equip_name]['embedding'][i]['value']])
                    # 生成描述信息
                    diamond_name = diamond_name + "提高" + str(value)
                    # 展示信息
                    self._setting_data[equip_name]['embedding'][i]['QLabel'].setText(diamond_name)
                    # 设置对应装备对象的属性
                    self.equip[equip_name].embedding[f"embedding_{i}"] = \
                        self._setting_data[equip_name]['embedding'][i]['value']

            # 计算精炼部分
            _strength = self._setting_data[equip_name]['strength']
            if _strength['QSpinBox'].value() != _strength['value']:
                # 设置新的精炼属性
                _strength['value'] = _strength['QSpinBox'].value()
            # 设置对应装备对象的属性
            self.equip[equip_name]: Equip
            # 这里加了最大精炼等级的影响
            self.equip[equip_name].strength = min(_strength['value'], self.equip[equip_name].max_strength_level)
            self.equip[equip_name].set_name()
            # 测试用
            # print(self.equip[equip_name])


    def _set_save_button_from_config(self):
        """
        读取config中的预设按钮项并配置到ui中
        1. 修改ui按钮名称
        2. 加载到QComboBox
        :return:
        """

        for index in range(1, 4):
            button_name = self.config[f"saving_button_{index}"]
            if button_name is not None:
                button: QPushButton = getattr(self.ui, f"savesetting_{index}_button")
                button.setText(button_name)
                self._combobox_items[index] = button_name
                self._combobox_reversed[button_name] = index
        self.ui.loadsetting_comboBox.clear()
        self.ui.loadsetting_comboBox.addItems([i for i in self._combobox_items.values() if i is not None])

