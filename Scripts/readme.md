# 剑网3苍云助手逻辑结构  
## 1. Config
> * config.py -> 设置模块  
## 2. GetData  
> * ...  
## 3. JclAnalysis    
> * analysis_main.py -> jcl分析模块顶层  
> ### 1. CountSkill    
>> * skill_data_reshape.py -> 函数库, 用于为表格整理数据  
> ### 2. GetMark  
>> * used_events.py -> 评分用数据
> ### 3. ImitationPlayer  
>> * player.py -> 读取buff状态, 记录技能释放时所存在的buff供复盘和评价使用  
## 4. ReadData  
> * reader_main -> jcl读取模块顶层
> ### 1. Equips
>> * attribute_calc.py -> 装备属性计算
>> * equip_reader.py -> 装备读取
>> * equip_type.py -> 自定义装备对象, 用于储存装备信息和方法
>> * get_other_data.py -> 补充读取未存在于数据中的装备和buff/技能数据
> ### 2. FileReader
>> * file_reader.py -> 读取jcl文件
>> * type_reader.py -> 针对jcl文件每行类型进行原始整理
## 5. UI
> * ui_main.py -> 顶层ui类, 负责ui初始化及下层页面调用
> ### 1. UI_Base
>> * ui.py -> .ui文件
>> * ui_base.py -> ui页面基类, 存放部分模块和公共弹窗
>> * ui_other.py -> ui页面部分常量和函数
>> * ui_style.py -> ui界面基本风格化, 窗口透明等
> ### 2. UI_Type
>> * ui_calculator.py -> 计算器页面功能实现
>> * ui_equip_setting.py -> 精炼镶嵌设置页面功能实现
>> * ui_retro.py -> 复盘页面功能实现
>> * ui_top.py -> 首页部分功能实现
## 6. PictureGeneration
> * pics_setting.py -> 图片生成模块的基础设置和公用变量
> * pics_equips.py -> 配装图片
 