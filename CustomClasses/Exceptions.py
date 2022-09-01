"""
用于项目中需要抛出的各类异常
供最终弹窗处理
"""
class NotFoundPlayerIDFromName(Exception): """未能从玩家名称查询到玩家id"""
class PlayerKungFuError(Exception): """玩家id所对应心法并不为苍云内功"""
class JclTypeError(Exception): """jcl文件格式未知错误,请联系开发者!"""
class JclFileEncodeError(Exception): """jcl文件编码已损坏，请更换其他记录吧！"""
class NotFoundJx3GameError(Exception): """未能读取到游戏路径，请手动选择！"""
class NotFoundJclFileError(Exception): """未能读取到Jcl文件，请手动选择！"""
class NotFoundJclFolderError(Exception): """未能读取到Jcl文件夹，请检查设置！"""
class JclFileTypeError(Exception): """当前文件并非jcl文件"""
class SourceNotFoundError(Exception): """未查询到复盘所需资源"""