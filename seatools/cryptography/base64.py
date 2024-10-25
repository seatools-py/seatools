from typing import Union, Optional, Any
import base64
from .base import _convert_data
import sys

_encode_handler_map = {
    '16': base64.b16encode,
    '32': base64.b32encode,
    '64': base64.b64encode,
    '85': base64.b85encode,
}

_decode_handler_map = {
    '16': base64.b16decode,
    '32': base64.b32decode,
    '64': base64.b64decode,
    '85': base64.b85decode,
}


def _common_encode_base(data: Union[str, bytes],
                        encoding='utf-8',
                        digit: str = '64') -> bytes:
    data = _convert_data(data, encoding)
    return _encode_handler_map[digit](data)


def _common_decode_base(data: Union[str, bytes],
                        encoding='utf-8',
                        digit: str = '64',
                        *,
                        casefold=False,
                        map01=None,
                        altchars=None,
                        validate=False) -> bytes:
    data = _convert_data(data, encoding)
    kwargs = {}
    if casefold:
        kwargs['casefold'] = True
    if map01:
        kwargs['map01'] = map01
    if altchars:
        kwargs['altchars'] = altchars
    if validate:
        kwargs['validate'] = validate
    return _decode_handler_map[digit](data, **kwargs)


def encode_base16(data: Union[str, bytes],
                  encoding='utf-8') -> bytes:
    """BASE16 编码"""
    return _common_encode_base(data, encoding, '16')


def encode_base32(data: Union[str, bytes],
                  encoding='utf-8') -> bytes:
    """BASE32 编码"""
    return _common_encode_base(data, encoding, '32')


def encode_base64(data: Union[str, bytes],
                  encoding='utf-8') -> bytes:
    """BASE64 编码"""
    return _common_encode_base(data, encoding, '64')


def encode_base85(data: Union[str, bytes],
                  encoding='utf-8') -> bytes:
    """BASE85 编码"""
    return _common_encode_base(data, encoding, '85')


def decode_base16(data: Union[str, bytes],
                  encoding='utf-8',
                  casefold=False) -> bytes:
    """BASE16 解码"""
    return _common_decode_base(data, encoding, '16',
                               casefold=casefold)


def decode_base32(data: Union[str, bytes],
                  encoding='utf-8',
                  casefold=False,
                  map01: Optional[bytes] = None) -> bytes:
    """BASE32 解码"""
    return _common_decode_base(data, encoding, '32',
                               casefold=casefold,
                               map01=map01)


def decode_base64(data: Union[str, bytes],
                  encoding='utf-8',
                  altchars: Any = None,
                  validate: bool = False) -> bytes:
    """BASE64 解码"""
    return _common_decode_base(data, encoding, '64',
                               altchars=altchars,
                               validate=validate)


def decode_base85(data: Union[str, bytes],
                  encoding='utf-8') -> bytes:
    """BASE85 解码"""
    return _common_decode_base(data, encoding, '85')


if sys.version_info >= (3, 10):
    _encode_handler_map['hex32'] = base64.b32hexencode
    _decode_handler_map['hex32'] = base64.b32hexdecode

    def encode_base32hex(data: Union[str, bytes],
                         encoding='utf-8') -> bytes:
        """BASE32 HEX 编码"""
        return _common_encode_base(data, encoding, 'hex32')

    def decode_base32hex(data: Union[str, bytes],
                         encoding='utf-8',
                         casefold=False) -> bytes:
        """BASE32 HEX 解码"""
        return _common_decode_base(data, encoding, 'hex32',
                                   casefold=casefold)
