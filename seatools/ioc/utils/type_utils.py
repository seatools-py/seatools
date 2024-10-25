from typing import Type


def is_basic_type(_type: Type):
    """判断是否是python基本数据类型, 包括tuple, list, dict"""
    return _type in (int, float, str, bool, bytes, bytearray, complex, tuple, list, dict)
