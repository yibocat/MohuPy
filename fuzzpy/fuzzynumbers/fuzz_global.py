#  Copyright (C) yibocat 2023 all Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/17 下午4:43
#  Author: yibow
#  E-mail: yibocat@yeah.net
#  Software: fuzzpy

def _init():
    """在主模块初始化"""
    global GLOBALS_DICT
    GLOBALS_DICT = {}


def global_set(name, value):
    """设置"""
    try:
        GLOBALS_DICT[name] = value
        return True
    except KeyError:
        return False


def global_get(name):
    """取值"""
    try:
        return GLOBALS_DICT[name]
    except KeyError:
        return "Not Found"


def global_dict():
    """获取字典"""
    return GLOBALS_DICT
