"""
用于项目中所用到的特殊类型的标注
"""
from typing import Any, Dict


class LuaTable:
    def __iter__(self): ...
    def __getitem__(self, item): ...


class Equip:
    """Scripts.ReadData.Equips.equip_type._Equip"""
    def __init__(self, data): ...
    def __call__(self, *args, **kwargs): ...
    def set_info(self): ...
    def read_embedding_and_strength(self): ...
    def set_name(self): ...
    equip_data: Any
    id: Any
    strength: Any  # 精炼
    max_strength_level: Any     # 最大精炼
    embedding: Any  # 镶嵌
    enhance: Any  # 小附魔
    enhance_name: Any
    enchant: Any  # 大附魔
    stone: Any   # 五彩石
    attrs: Any
    changed_attrs: Any  # 精炼镶嵌
    subtype: Any  # 子类型. 即表的名称
    name: Any
    equip_type: Any  # 散件/精简/无皇/特效
    level: Any  # 品级
    attr_type: Any  # 简要属性，_Attrs


class PlayerEquip:
    """Scripts/ReadData/Equips/equip_reader.py"""
    def __init__(self): ...
    def __getitem__(self, item): ...
    def set_equip(self): ...


class Attribute:
    """Scripts/ReadData/Equips/attribute_calc.py"""
    def __init__(self, equip): ...
    def __getitem__(self, item): ...
    def __str__(self): ...
    def calc_attribute(self): ...
    json_attributes: Any
    embedding_count: Any
    player_kungfu: Any
    player_talent: list

# class ConfigSetting:
#     """Scripts/Config/config.py"""
#     def __init__(self): ...
#     def add_config(self, section: str, key: str, value: Any): ...
#     def config(self) -> list: ...


class FileReader:
    """Scripts/ReadData/reader_main.py"""
    def __init__(self): ...
    @property
    def player_id(self) -> int: return ...
    @property
    def npc_id(self) -> list: return ...
    @property
    def data(self): return
    @property
    def csv_data(self): return
    @property
    def equip(self) -> dict: return ...
    @property
    def json_attribute(self) -> dict: return ...
    @property
    def attribute(self) -> Attribute: return ...
    @property
    def id_to_name(self) -> dict: return ...


class Player:
    """Scripts/JclAnalysis/ImitationPlayer/player.py"""
    def __init__(self): ...
    @property
    def skill_events_by_time(self) -> Dict: ...
    @property
    def skill_events_by_id(self) -> Dict: ...
    player_id: Any
    npc_id: Any