实用工具
========

加密工具
--------

提供常用的加密算法:

.. code-block:: python

   from seatools.cryptography import md5, encode_base64, sha256_hmac

   # MD5 加密
   md5_hash = md5('test')

   # Base64 编码
   base64_str = encode_base64('test')

   # HMAC SHA256
   hmac_hash = sha256_hmac('key', 'message')

重试机制
--------

支持同步和异步的重试机制:

.. code-block:: python

   from seatools.retry import Retry, AsyncRetry

   retry = Retry(
       max_attempts=3,
       delay=1,
       log_enable=True
   )

   @retry.retry
   def may_fail():
       # 可能失败的操作
       pass

缓存工具
--------

提供内存缓存支持:

.. code-block:: python

   from seatools.cache import Cache

   cache = Cache()

   @cache.cache(key='user-${user_id}')
   def get_user(user_id: int):
       # 获取用户信息
       pass

日志工具
--------

基于 loguru 的日志工具:

.. code-block:: python

   from seatools.logger import setup
   from loguru import logger

   setup(
       'app.log',
       rotation='1 days',
       retention='30 days'
   )

   logger.info('info message')
   logger.error('error message')
