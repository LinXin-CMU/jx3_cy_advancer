from configparser import ConfigParser
from typing import Any
from os.path import exists
from threading import Lock


class ConfigSetting:
    """
    设置config文件的类
    """
    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return getattr(cls, '_instance')


    def __init__(self):
        self.path = r'Sources\Settings\config.ini'
        # config文件存放路径
        self.cf = ConfigParser()
        self.lock = Lock()
        # 保护单例模式的线程安全
        if not exists(self.path):
            with open(self.path, 'w+', encoding='utf-8') as f:
                self.cf.read_file(f)
        else:
            self.cf.read(self.path, encoding='utf-8')


    def __getitem__(self, item):
        for sec in self.cf.sections():
            if item in self.cf.options(sec):
                return self.cf.get(sec, item)
        return None


    def add_config(self, section: str, key: str, value: Any):
        self.lock.acquire()
        count = 0
        while count < 5:
            count += 1
            if not isinstance(value, str):
                try:
                    value = value.__repr__()
                except AttributeError:
                    value = str(value)
            else:
                break
        if section not in self.cf.sections():
            self.cf.add_section(section)
        self.cf.set(section=section, option=key.upper(), value=value)
        self.cf.write(open(self.path, 'w', encoding='utf-8'))
        self.lock.release()


    @property
    def config(self):
        return [self.cf.items(sec) for sec in self.cf.sections()]


