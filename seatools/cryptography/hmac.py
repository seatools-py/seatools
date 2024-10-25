import hashlib
import hmac as hmac
from typing import Union
from .base import _convert_data


def _common_hmac(key: Union[str, bytes],
                 data: Union[str, bytes, None] = None,
                 digestmod: Union[str, callable] = '',
                 encoding='utf-8') -> bytes:
    key = _convert_data(key, encoding=encoding)
    if data:
        data = _convert_data(data, encoding=encoding)
    return hmac.new(key, data, digestmod).digest()


def md5_hmac(key: Union[str, bytes],
             data: Union[str, bytes, None] = None,
             encoding='utf-8') -> bytes:
    """MD5 HMAC 加密"""
    return _common_hmac(key, data, hashlib.md5,
                        encoding=encoding)


def sha1_hmac(key: Union[str, bytes],
              data: Union[str, bytes, None] = None,
              encoding='utf-8') -> bytes:
    """SHA1 HMAC 加密"""
    return _common_hmac(key, data, hashlib.sha1,
                        encoding=encoding)


def sha224_hmac(key: Union[str, bytes],
                data: Union[str, bytes, None] = None,
                encoding='utf-8') -> bytes:
    """SHA224 HMAC"""
    return _common_hmac(key, data, hashlib.sha224,
                        encoding=encoding)


def sha256_hmac(key: Union[str, bytes],
                data: Union[str, bytes, None] = None,
                encoding='utf-8') -> bytes:
    """SHA256 HMAC 加密"""
    return _common_hmac(key, data, hashlib.sha256,
                        encoding=encoding)


def sha384_hmac(key: Union[str, bytes],
                data: Union[str, bytes, None] = None,
                encoding='utf-8') -> bytes:
    """SHA384 HMAC 加密"""
    return _common_hmac(key, data, hashlib.sha384,
                        encoding=encoding)


def sha512_hmac(key: Union[str, bytes],
                data: Union[str, bytes, None] = None,
                encoding='utf-8') -> bytes:
    """SHA512 HMAC 加密"""
    return _common_hmac(key, data, hashlib.sha512,
                        encoding=encoding)
