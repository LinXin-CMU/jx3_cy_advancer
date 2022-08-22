# coding: utf-8
# author: LinXin
"""
从jx3box获取其他未在数据库中的数据
"""
from threading import Thread, Lock
import requests
from typing import Literal

personal_data = {}
lock = Lock()

def write_in(subtype):
    _subtype = subtype
    def for_subtypes(func):
        def wrapper(*args, **kwargs):
            global lock
            lock.acquire()
            with open(r'Sources/Settings/personal_data', 'a', encoding='utf-8') as f:
                ret = func(*args, **kwargs)
                if ret is not None:
                    f.write([_subtype, ret['ID'], ret['Data']].__repr__() + "\n")
            lock.release()
            return ret
        return wrapper
    return for_subtypes



def get_equip_from_jx3box(subtype: Literal["armor", "trinket", "weapon"], id: int):

    global personal_data

    if subtype in personal_data:
        if id in personal_data[subtype]:
            ret = {'ID': id, 'Data': personal_data[subtype][id]}
            return ret

    url = f"https://node.jx3box.com/equip/{subtype}?client=std&id={id}"
    ret = None

    @write_in(subtype)
    def _get():
        nonlocal ret
        resp = requests.get(url=url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()['list'][0]
            ret = {'ID': data['ID'], 'Data': data}
            return ret

    thread = Thread(target=_get, daemon=True)
    thread.start()
    thread.join()

    return ret


def get_buff_or_skill_from_jx3box(subtype: Literal["buff", "skill"], id: int, level: int) -> dict:

    global personal_data
    if subtype in personal_data:
        if id in personal_data[subtype]:
            if level in personal_data[subtype][id]:
                ret = personal_data[subtype][id][level]
                return ret

    url = f"https://node.jx3box.com/{subtype}/id/{id}?client=std&level={level}"
    url2 = f"https://node.jx3box.com/{subtype}/id/{id}?client=std"
    ret = {'ID': id, 'Data': {level: {'Name': f'未知{subtype}'}}}

    @write_in(subtype)
    def _get():
        nonlocal ret
        resp = requests.get(url=url, timeout=3)
        if resp.status_code == 200:
            try:
                data = resp.json()['list'][0]
            except IndexError:
                resp = requests.get(url=url2, timeout=3)
                if resp.status_code == 200:
                    try:
                        data = resp.json()['list'][0]
                    except IndexError:
                        data = None
                else:
                    data = None
            if data is not None:
                ret = {'ID': id, 'Data': {level: {"Remark": data['Remark'], "Name": data['Name'], f"{subtype.capitalize()}Name": data[f'{subtype.capitalize()}Name'], "Desc": data['Desc']}}}
            return ret

    thread = Thread(target=_get, daemon=True)
    thread.start()
    thread.join()

    return ret['Data'][level]


def __read_personal_data():
    """
    从Sources/Settings/personal_data中读取出现有的数据\n
    :return:
    """
    global personal_data, lock
    lock.acquire()
    with open(r'Sources/Settings/personal_data', 'r', encoding='utf-8') as f:
        data = [eval(i.strip()) for i in f.readlines()]
        for item in data:
            _location = item[0]
            _id = item[1]
            _data = item[2]
            if _location == 'buff':
                if _location not in personal_data:
                    personal_data[_location] = {_id: _data}
                elif _id in personal_data:
                    personal_data[_location][_id].update(_data)
                else:
                    personal_data[_location][_id] = _data
            elif _location not in personal_data:
                personal_data[_location] = {_id: _data}
            else:
                personal_data[_location][_id] = _data
    lock.release()


if __name__ == 'Scripts.ReadData.Equips.get_other_data':
    __read_personal_data()
