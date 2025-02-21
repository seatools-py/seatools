重试机制
=======

同步重试
-------

支持同步函数的重试机制:

.. code-block:: python

   from seatools.retry import Retry

   retry = Retry(
       max_attempts=3,  # 最大重试次数
       delay=1,         # 重试间隔(秒)
       log_enable=True  # 启用日志
   )

   @retry.retry
   def may_fail():
       # 可能失败的操作
       pass

异步重试
-------

支持异步函数的重试机制:

.. code-block:: python

   from seatools.retry import AsyncRetry

   retry = AsyncRetry(
       max_attempts=3,
       delay=1,
       log_enable=True
   )

   @retry.retry
   async def may_fail():
       # 可能失败的异步操作
       pass
