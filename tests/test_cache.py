import asyncio
import json

import pytest

from seatools.cache import Cache, AsyncCache, TTLCache
from seatools.cache.ext import SqliteCache
from loguru import logger
from seatools.models import BaseModel


cache = Cache(cache=TTLCache(maxsize=100, ttl=60), debug=True)
async_cache = AsyncCache(cache=TTLCache(maxsize=100, ttl=60), debug=True)


class D(BaseModel):
    a: int


@cache.cacheable(key='func1_${a}_${b}')
def func1(a: int, b: str):
    return f'{a}_{b}'


@cache.cache_evict(key='func1_${a}_${b}')
def clear_func1_cache(a: int, b: str):
    pass


@cache.cache_put(key='func1_${a}_${b}')
def put_func1_cache(a: int, b: str):
    return f'{a}_{b}'


@cache.cache_put(key='func_${s.1}')
def put_list_cache(s: list):
    return json.dumps(s)


@cache.cache_put(key='func_${s.s}')
def put_list_error_cache(s: list):
    return json.dumps(s)


class A:

    def __init__(self, a=1):
        self.a = a


@cache.cache_put('object_${a.a}')
def put_a(a: A):
    pass

@cache.cache_put('object_${a.b}')
def put_b(a: A):
    pass


def test_cache():
    v1 = put_func1_cache(1, 's')
    v1 = func1(1, 's', D(a=123))
    logger.info("v1: {}", v1)
    clear_func1_cache(1, 's')
    v2 = func1(1, 's')
    logger.info("v2: {}", v2)
    put_list_cache([1,2,3])
    cache.put('x', None)
    cache.get('x')
    cache.clear()
    with pytest.raises((IndexError, ValueError)):
        put_list_cache([1])
    with pytest.raises(ValueError):
        put_list_error_cache([1, 's'])
    put_a(A(a=2))
    with pytest.raises((AttributeError, ValueError)):
        put_b(A(a=2))




@async_cache.cacheable(key='func1_${a}_${b}')
async def async_func1(a: int, b: str):
    return f'{a}_{b}'


@cache.cacheable(key='func1_${a}_${b}')
async def async_func2(a: int, b: str):
    return f'{a}_{b}'


@async_cache.cache_evict(key='func1_${a}_${b}')
async def async_clear_func1_cache(a: int, b: str):
    pass


@async_cache.cache_put(key='func1_${a}_${b}')
async def async_put_func1_cache(a: int, b: str):
    return f'{a}_{b}'


@cache.cache_evict(key='func1_${a}_${b}')
async def async_clear_func2_cache(a: int, b: str):
    pass


@cache.cache_put(key='func1_${a}_${b}')
async def async_put_func2_cache(a: int, b: str):
    return f'{a}_{b}'


def test_async_cache():
    v1 = asyncio.run(async_put_func1_cache(1, 's'))
    v1 = asyncio.run(async_func1(1, 's'))
    logger.info("v1: {}", v1)
    asyncio.run(async_clear_func1_cache(1, 's'))
    v2 = asyncio.run(async_func1(1, 's'))
    logger.info("v2: {}", v2)


def test_async_cache2():
    v1 = asyncio.run(async_put_func2_cache(1, 's'))
    v1 = asyncio.run(async_func2(1, 's'))
    logger.info("v1: {}", v1)
    asyncio.run(async_clear_func2_cache(1, 's'))
    v2 = asyncio.run(async_func2(1, 's'))
    logger.info("v2: {}", v2)


def test_sqlite_cache(tmp_path):
    ori_sqlite_cache = SqliteCache(conn_url=f'sqlite:///tmp/cache.db', maxsize=100)
    sqlite_cache = Cache(cache=ori_sqlite_cache, debug=True)
    sqlite_cache.put('a', 1234)
    v = sqlite_cache.get('a')
    logger.info('a: {}', v)
    sqlite_cache.evict('a')
    v = sqlite_cache.get('a')
    logger.info('a: {}', v)
    with pytest.raises(KeyError):
        logger.info(ori_sqlite_cache['xxx'])
