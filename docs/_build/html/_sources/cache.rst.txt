缓存支持
========

内存缓存
---------

提供基于内存的缓存支持:

.. code-block:: python

   from seatools.cache import Cache

   cache = Cache()

   # 基于键值的缓存
   @cache.cache(key='user-${user_id}', ttl=3600)
   def get_user(user_id: int):
       return user_dao.get(user_id)

   # 清除缓存
   cache.clear('user-1')

   # 清除所有缓存
   cache.clear_all()

分布式缓存
-----------

使用前需要安装redis依赖:

.. code-block:: bash

   pip install redis

基于 Redis 的分布式缓存支持:

.. code-block:: python

   from seatools.cache import RedisCache

   cache = RedisCache(
       host='localhost',
       port=6379,
       db=0
   )

   @cache.cache(key='user-${user_id}', ttl=3600)
   def get_user(user_id: int):
       return user_dao.get(user_id)
