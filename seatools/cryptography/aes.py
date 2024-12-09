from typing import Tuple

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_aes(data: bytes, key: bytes, *args, **kwargs) -> Tuple[bytes, bytes]:
    """AES 加密

    Args:
        data: 数据
        key: 加密key

    Returns:
        加密后的bytes与iv值
    """
    cipher = AES.new(key, AES.MODE_CBC, *args, **kwargs)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    return ciphertext, iv


def decrypt_aes(ciphertext: bytes, key: bytes, iv: bytes=None, *args, **kwargs) -> bytes:
    """AES 解密

    Args:
        ciphertext: 解密串bytes
        iv: iv值
        key: 加密的key

    Returns:
        解密后的数据
    """
    cipher = AES.new(key, AES.MODE_CBC, iv=iv, *args, **kwargs)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext
