import hashlib
from typing import Union
from enum import Enum
from .base import _convert_data


def _md5_16(data: bytes):
    # 计算32位MD5哈希值
    return hashlib.md5(data).hexdigest()[8:-8]


def _md5_32(data: bytes):
    # 计算32位MD5哈希值
    return hashlib.md5(data).hexdigest()


def _md5_64(data: bytes):
    # 计算32位MD5哈希值
    return hashlib.md5(data).hexdigest() * 2


class Md5DigitEnum(Enum):
    MD5_16 = 16
    MD5_32 = 32
    MD5_64 = 64


_DIGIT_HANDLE_MAP = {
    Md5DigitEnum.MD5_16: _md5_16,
    Md5DigitEnum.MD5_32: _md5_32,
    Md5DigitEnum.MD5_64: _md5_64,
}


def md5(data: Union[str, bytes],
        encoding='utf-8',
        digit: Md5DigitEnum = Md5DigitEnum.MD5_32) -> str:
    """MD5 加密工具

    Args:
        data: 需要加密的数据
        encoding: 数据的字符集类型
        digit: 加密的位数
    """
    data = _convert_data(data, encoding)
    handle = _DIGIT_HANDLE_MAP.get(digit)
    if not handle:
        raise ValueError('不支持的md5加密位数: {}'.format(digit))
    return handle(data)
