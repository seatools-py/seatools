import pytest

from seatools.cryptography.aes import encrypt_aes, decrypt_aes
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES


def test_aes():
    # 测试用的密钥和数据
    KEY = get_random_bytes(16)  # AES-128位密钥
    IV = get_random_bytes(AES.block_size)  # 初始向量
    DATA = 'This is a top secret message.'
    data, iv = encrypt_aes(DATA.encode('utf-8'), KEY, iv=IV)
    assert data, 'AES encrypted data'
    ori_data = decrypt_aes(data, KEY, iv=iv).decode('utf-8')
    assert ori_data == DATA, 'AES decrypted data error'


def test_md5():
    from seatools.cryptography import md5, Md5DigitEnum
    text = '123456'
    assert md5(text) == 'e10adc3949ba59abbe56e057f20f883e'
    assert md5(text, digit=Md5DigitEnum.MD5_16) == '49ba59abbe56e057'
    assert md5(text, digit=Md5DigitEnum.MD5_64) == md5(text) + md5(text)
    with pytest.raises(ValueError):
        print(md5(text, digit=66))


def test_base64():
    from seatools.cryptography import encode_base16, encode_base32, encode_base64, encode_base85, encode_base32hex, \
        decode_base16, decode_base32, decode_base64, decode_base85, decode_base32hex
    text = '123456'
    assert encode_base64(text).decode('utf-8') == 'MTIzNDU2'
    assert encode_base16(text).decode('utf-8') == '313233343536'
    assert encode_base32(text).decode('utf-8') == 'GEZDGNBVGY======'
    assert encode_base32hex(text).decode('utf-8') == '64P36D1L6O======'
    assert encode_base85(text).decode('utf-8') == 'F)}kWH8u'

    assert decode_base64('MTIzNDU2').decode('utf-8') == text
    assert decode_base16('313233343536').decode('utf-8') == text
    assert decode_base32('GEZDGNBVGY======').decode('utf-8') == text
    assert decode_base32hex('64P36D1L6O======').decode('utf-8') == text
    assert decode_base85('F)}kWH8u').decode('utf-8') == text


def test_mac():
    # todo:
    pass
