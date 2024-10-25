import re
from cachetools import Cache as _Cache
import inspect
from typing import Any
from loguru import logger


class _BaseCache:

    def __init__(self, cache: _Cache, debug=False):
        """
        Args:
            cache: 缓存管理对象
            debug: 调试模式, 调试模式会设置日志
        """
        self._cache = cache
        self._none = object()
        self._debug = debug

    def _wrapper_data(self, data):
        if data is None:
            return self._none
        return data

    def _unwrapper_data(self, data):
        if data is self._none:
            return None
        return data

    def _get_key_name_value(self, obj, key: str):
        keys = key.split('.')
        for k in keys:
            if isinstance(obj, dict):
                obj = obj.get(k, self._none)
            elif isinstance(obj, (list, tuple)):
                try:
                    try:
                        # 尝试解析指定索引
                        obj = obj[int(k)]
                    except ValueError:
                        # 否则取数组第一个元素然后尝试继续解析名称k
                        obj = obj[0]
                        obj = self._get_key_name_value(obj, k)
                except IndexError:
                    obj = self._none
            else:
                try:
                    obj = getattr(obj, k)
                except AttributeError:
                    obj = self._none
            if obj is self._none:
                raise ValueError('缓存key[{}]中的属性[{}]不存在'.format(key, k))
        return obj

    def _gen_key(self, func, key, *args, **kwargs) -> str:
        """
        将key中的变量值进行替换
        """
        mapping = {k: v for k, v in kwargs.items()}
        # args映射
        if args:
            signature = inspect.signature(func)
            names = list(signature.parameters.keys())
            for i in range(min(len(names), len(args))):
                mapping[names[i]] = args[i]
        # 定义正则表达式匹配${}包含的内容
        pattern = r'\${(.*?)}'
        # 使用正则表达式查找所有匹配的内容
        matches = re.findall(pattern, key)
        # 遍历匹配结果
        for match in matches:
            # 如果匹配到的内容在字典中存在对应的映射，则进行替换
            key = key.replace(f'${{{match}}}', str(self._get_key_name_value(mapping, match)))
        return key

    def put(self, key: str, data: Any):
        """设置缓存

        Args:
            key: 缓存的key
            data: 缓存的数据
        """
        self._debug_msg('设置缓存key[{}], 值: {}', key, data)
        self._cache[key] = self._wrapper_data(data)

    def get(self, key: str, default=None) -> Any:
        """获取缓存值

        Args:
            key: 缓存的key值
            default: 若缓存不存在数据, 则返回的默认值

        Returns:
            若该缓存存在, 则返回该返回的值, 否则返回default默认值
        """
        data = self._unwrapper_data(self._cache.get(key, default=default))
        self._debug_msg('获取缓存key[{}], 值: {}', key, data)
        return data

    def evict(self, key: str, default=None) -> Any:
        """清除缓存

        Args:
            key: 缓存的key
            default: 若缓存不存在数据, 则返回的默认值
        Returns:
            若该缓存存在, 则返回该返回的值, 否则返回default默认值
        """
        data = self._unwrapper_data(self._cache.pop(key, default=default))
        self._debug_msg('删除缓存key[{}], 值: {}', key, data)
        return data

    def clear(self):
        """清空所有缓存"""
        self._cache.clear()
        self._debug_msg('清空所有缓存')

    def _debug_msg(self, msg: str, *args, **kwargs):
        if self._debug:
            logger.debug(msg, *args, **kwargs)


class Cache(_BaseCache):

    def __init__(self, cache: _Cache, debug=False):
        super().__init__(cache, debug)

    def cacheable(self, key: str):
        """缓存查询装饰器, 参数变量使用${参数名}填充
        使用示例:
            from cachetools import TTLCache

            cache = Cache(cache=TTLCache(maxsize=1024, ttl=600))

            @cache.cacheable(key='xxx_${a}_${b}')
            def xxx(a: int, b: str):
                # 业务逻辑

            # 调用
            v = xxx(1, 's') # 第一次调用将结果设置到key为 xxx_1_s 的缓存上, 再次调用将直接返回缓存结果

        Args:
            key: key的表达式, 使用函数的变量使用${}包裹
        """

        def wrapper_func(func):
            def wrapper(*args, **kwargs):
                _key = self._gen_key(func, key, *args, **kwargs)
                data = self._cache.get(_key)
                if data is not None:
                    data = self._unwrapper_data(data)
                    self._debug_msg('获取缓存key[{}], 值: {}', _key, data)
                    return data
                data = func(*args, **kwargs)
                self.put(_key, data)
                return data

            return wrapper

        return wrapper_func

    def cache_put(self, key: str):
        """缓存设置装饰器, 参数变量使用${参数名}填充
        使用示例:
            from cachetools import TTLCache

            cache = Cache(cache=TTLCache(maxsize=1024, ttl=600))

            @cache.cache_put(key='xxx_${a}_${b}')
            def xxx(a: int, b: str):
                # 业务逻辑

            # 调用
            xxx(1, 's') # 每次调用都将方法返回的结果 设置到缓存key为 xxx_1_s 上
        """

        def wrapper_func(func):
            def wrapper(*args, **kwargs):
                _key = self._gen_key(func, key, *args, **kwargs)
                data = func(*args, **kwargs)
                self.put(_key, data)
                return data

            return wrapper

        return wrapper_func

    def cache_evict(self, key: str):
        """缓存清除装饰器, 参数变量使用${参数名}填充
        使用示例:
            from cachetools import TTLCache

            cache = Cache(cache=TTLCache(maxsize=1024, ttl=600))

            @cache.cache_evict(key='xxx_${a}_${b}')
            def xxx(a: int, b: str):
                # 业务逻辑

            # 调用
            xxx(1, 's') # 清除key为 xxx_1_s 的缓存

        Args:
            key: key的表达式, 使用函数的变量使用${}包裹
        """

        def wrapper_func(func):
            def wrapper(*args, **kwargs):
                _key = self._gen_key(func, key, *args, **kwargs)
                self.evict(_key, default=None)
                return func(*args, **kwargs)

            return wrapper

        return wrapper_func


class AsyncCache(_BaseCache):

    def __init__(self, cache: _Cache, debug=False):
        super().__init__(cache, debug)

    def cacheable(self, key: str):
        """缓存查询装饰器, 参数变量使用${参数名}填充
        使用示例:
            from cachetools import TTLCache

            async_cache = AsyncCache(cache=TTLCache(maxsize=1024, ttl=600))

            @async_cache.cacheable(key='xxx_${a}_${b}')
            async def xxx(a: int, b: str):
                # 业务逻辑

            # 调用
            v = xxx(1, 's') # 第一次调用将结果设置到key为 xxx_1_s 的缓存上, 再次调用将直接返回缓存结果

        Args:
            key: key的表达式, 使用函数的变量使用${}包裹
        """

        def wrapper_func(async_func):
            async def wrapper(*args, **kwargs):
                _key = self._gen_key(async_func, key, *args, **kwargs)
                data = self._cache.get(_key)
                if data is not None:
                    data = self._unwrapper_data(data)
                    self._debug_msg('获取缓存key[{}], 值: {}', _key, data)
                    return data
                data = await async_func(*args, **kwargs)
                self.put(_key, data)
                return data

            return wrapper

        return wrapper_func

    def cache_put(self, key: str):
        """缓存设置装饰器, 参数变量使用${参数名}填充
        使用示例:
            from cachetools import TTLCache

            async_cache = AsyncCache(cache=TTLCache(maxsize=1024, ttl=600))

            @async_cache.cache_put(key='xxx_${a}_${b}')
            def xxx(a: int, b: str):
                # 业务逻辑

            # 调用
            xxx(1, 's') # 每次调用都将方法返回的结果 设置到缓存key为 xxx_1_s 上
        """

        def wrapper_func(async_func):
            async def wrapper(*args, **kwargs):
                _key = self._gen_key(async_func, key, *args, **kwargs)
                data = await async_func(*args, **kwargs)
                self.put(_key, data)
                return data

            return wrapper

        return wrapper_func

    def cache_evict(self, key: str):
        """缓存清除装饰器, 参数变量使用${参数名}填充
        使用示例:
            from cachetools import TTLCache

            async_cache = AsyncCache(cache=TTLCache(maxsize=1024, ttl=600))

            @async_cache.cache_evict(key='xxx_${a}_${b}')
            def xxx(a: int, b: str):
                # 业务逻辑

            # 调用
            xxx(1, 's') # 清除key为 xxx_1_s 的缓存

        Args:
            key: key的表达式, 使用函数的变量使用${}包裹
        """

        def wrapper_func(async_func):
            async def wrapper(*args, **kwargs):
                _key = self._gen_key(async_func, key, *args, **kwargs)
                self.evict(_key, default=None)
                return await async_func(*args, **kwargs)

            return wrapper

        return wrapper_func
