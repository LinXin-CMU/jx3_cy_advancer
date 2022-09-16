# coding: utf-8
# author: LinXin
# 发送异常信息的邮件的模块

from yagmail import SMTP
from datetime import datetime
from typing import Dict


class TraceBackEmail:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self._user = "jx3_cy_advancer@163.com"
        self._password = "OVPTYXGUTESLSFNT"
        self._host = "smtp.163.com"

    def send(self, player_id: int, id_to_name: Dict, traceback_format: str, jcl_file_path: str):
        _server = SMTP(user=self._user, password=self._password, host=self._host)
        try:
            # 先获取角色名
            if player_id in id_to_name:
                player_id = id_to_name[player_id]
            _email_to = self._user
            _email_title = f"Error_{jcl_file_path.split('/')[-1].replace('.jcl', '')}"
            _email_content = f"""
                {datetime.now()}\n
                {player_id.__repr__()}\n
                {traceback_format}
                """
            try:
                _email_attachment = [jcl_file_path, ]
            except FileNotFoundError:
                _email_attachment = None
            _server.send(_email_to, _email_title, contents=_email_content, attachments=_email_attachment)
        finally:
            _server.close()





























