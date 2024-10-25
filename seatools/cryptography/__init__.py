from .md5 import Md5DigitEnum, md5
from .base64 import encode_base16, encode_base32, encode_base64, encode_base85, \
    decode_base16, decode_base32, decode_base64, decode_base85
from .hmac import md5_hmac, sha1_hmac, sha256_hmac, sha224_hmac, sha384_hmac, sha512_hmac

import sys
if sys.version_info >= (3, 10):
    from .base64 import encode_base32hex, decode_base32hex
