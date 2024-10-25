import asyncio

from seatools.cache import Cache, AsyncCache, TTLCache
from seatools.cache.ext import SqliteCache
from loguru import logger
from seatools.models import BaseModel


cache = Cache(cache=TTLCache(maxsize=100, ttl=60))
async_cache = AsyncCache(cache=TTLCache(maxsize=100, ttl=60))
sqlite_cache = Cache(cache=SqliteCache(maxsize=100), debug=True)


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


def test_cache():
    v1 = put_func1_cache(1, 's')
    v1 = func1(1, 's', D(a=123))
    logger.info("v1: {}", v1)
    clear_func1_cache(1, 's')
    v2 = func1(1, 's')
    logger.info("v2: {}", v2)


@async_cache.cacheable(key='func1_${a}_${b}')
async def async_func1(a: int, b: str):
    return f'{a}_{b}'


@async_cache.cache_evict(key='func1_${a}_${b}')
async def async_clear_func1_cache(a: int, b: str):
    pass


@async_cache.cache_put(key='func1_${a}_${b}')
async def async_put_func1_cache(a: int, b: str):
    return f'{a}_{b}'


def test_async_cache():
    v1 = asyncio.run(async_put_func1_cache(1, 's'))
    v1 = asyncio.run(async_func1(1, 's'))
    logger.info("v1: {}", v1)
    asyncio.run(async_clear_func1_cache(1, 's'))
    v2 = asyncio.run(async_func1(1, 's'))
    logger.info("v2: {}", v2)


def test_sqlite_cache():
    sqlite_cache.put('a', 1234)
    v = sqlite_cache.get('a')
    logger.info('a: {}', v)
    sqlite_cache.evict('a')
    v = sqlite_cache.get('a')
    logger.info('a: {}', v)
