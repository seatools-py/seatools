环境管理
========

多环境配置
----------

支持开发、测试、生产等多环境配置:

.. code-block:: python

   from seatools.env import get_env
   import os

   # 设置环境
   os.environ['ENV'] = 'dev'  # dev/test/pro

   env = get_env()

   # 判断当前环境
   if env.is_dev():
       # 开发环境配置
       pass
   elif env.is_test():
       # 测试环境配置
       pass
   elif env.is_pro():
       # 生产环境配置
       pass
