import asyncio

import pytest

from seatools.retry import Retry, AsyncRetry
from loguru import logger

cnt = 0

GLOBAL_RETRY = Retry(max_attempts=10,  # 最大重试次数
                     delay=1,  # 每次重试的等待间隔, 单位秒
                     log_enable=True,  # 是否打印日志
                     ever_fail_level='WARNING',  # 每次任务失败记录的日志级别(未达到重试上限),
                     fail_level='ERROR',  # 任务重试达到失败上限的日志级别
                     )

GLOBAL_ASYNC_RETRY = AsyncRetry(max_attempts=10,  # 最大重试次数
                                delay=1,  # 每次重试的等待间隔, 单位秒
                                log_enable=True,  # 是否打印日志
                                ever_fail_level='WARNING',  # 每次任务失败记录的日志级别(未达到重试上限),
                                fail_level='ERROR',  # 任务重试达到失败上限的日志级别
                                )


def fail3(a: int, b: int):
    logger.info('请求参数a: {}, b: {}', a, b)
    global cnt
    if cnt < 3:
        cnt += 1
        raise Exception('异常')
    logger.info('cnt: {}', cnt)
    return cnt


def test_retry():
    _retry = Retry(max_attempts=10,  # 最大重试次数
                   delay=1,  # 每次重试的等待间隔, 单位秒
                   log_enable=True,  # 是否打印日志
                   ever_fail_level='WARNING',  # 每次任务失败记录的日志级别(未达到重试上限),
                   fail_level='ERROR',  # 任务重试达到失败上限的日志级别
                   )
    logger.info(_retry.do(fail3, 1, b=5))


@GLOBAL_RETRY.retry
def fail3_wrapper(a: int, b: int):
    logger.info('请求参数a: {}, b: {}', a, b)
    global cnt
    if cnt < 3:
        cnt += 1
        raise Exception('异常')
    logger.info('cnt: {}', cnt)
    return cnt


def test_retry2():
    fail3_wrapper(1, 2)


async def test(a: int):
    raise Exception(f'异常{a}')


def test_async_retry():
    _async_retry = AsyncRetry(max_attempts=3,  # 最大重试次数
                              delay=1,  # 每次重试的等待间隔, 单位秒
                              log_enable=True,  # 是否打印日志
                              ever_fail_level='WARNING',  # 每次任务失败记录的日志级别(未达到重试上限),
                              fail_level='ERROR',  # 任务重试达到失败上限的日志级别
                              )
    with pytest.raises(Exception):
        asyncio.run(_async_retry.do(test, 3))


@GLOBAL_ASYNC_RETRY.retry
async def fail3_async_wrapper(a: int, b: int):
    logger.info('请求参数a: {}, b: {}', a, b)
    global cnt
    if cnt < 3:
        cnt += 1
        raise Exception('异常')
    logger.info('cnt: {}', cnt)
    return cnt


def test_async_retry2():
    asyncio.run(fail3_async_wrapper(1, 2))
