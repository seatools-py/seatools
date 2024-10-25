import time
from loguru import logger
from typing import Union, Tuple, TypeVar, Type

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

_T = TypeVar('_T', bound=Exception)


class _BaseRetry:
    """重试基类"""

    def __init__(self, max_attempts=3, delay=1,
                 allow_exceptions: Union[Type[_T], Tuple[Type[_T]]] = Exception,
                 ignore_exceptions: Union[Type[_T], Tuple[Type[_T]], None] = None,
                 log_enable: bool = True,
                 ever_fail_level: Literal['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'WARNING',
                 fail_level: Literal['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'ERROR'):
        """初始化重试工具

        Args:
            max_attempts (int): 最大重试次数，默认为 3 次。
            delay (float): 重试之间的延迟时间，单位为秒，默认为 1 秒。
            allow_exceptions: 允许重试的异常类型, 不能为空
            ignore_exceptions: 忽略重试的异常类型, 如果忽略重试的异常不为空, 则优先匹配忽略重试的异常
            log_enable: 是否记录日志
            ever_fail_level: 每次失败记录的日志级别
            fail_level: 全部失败记录的日志级别
        """
        self._max_attempts = max_attempts
        self._delay = delay
        self._log_enable = log_enable
        self._ever_fail_level = ever_fail_level
        self._fail_level = fail_level
        self._allow_exceptions = allow_exceptions
        self._ignore_exceptions = ignore_exceptions

    def _handle_attempt_error(self, attempt, func, e, *args, **kwargs):
        """处理一次重试失败

        Args:
            attempt: 第attempt次失败, 从1开始
            func: 执行的函数
            e: 发生的异常
            args: 执行的函数的args参数
            kwargs: 执行的函数的kwargs参数
        """
        # 需要过滤的异常则忽略重试
        if self._ignore_exceptions and isinstance(e, self._ignore_exceptions):
            raise e
        if attempt < self._max_attempts:
            if self._log_enable:
                logger.log(self._ever_fail_level,
                           "函数[{}]第[{}]次执行失败, 失败原因: {}, 等待[{}]秒后将进行重试, 函数参数args: {}, kwargs: {}",
                           func.__name__, attempt, e, self._delay, args, kwargs)
            time.sleep(self._delay)
        else:
            if self._log_enable:
                logger.log(self._fail_level,
                           '函数[{}]重试[{}]次仍然失败, 抛出异常: {}, 函数参数args: {}, kwargs: {}',
                           func.__name__, self._max_attempts, e, args, kwargs)
            raise e


class Retry(_BaseRetry):
    """重试工具"""

    def __init__(self, max_attempts=3, delay=1,
                 allow_exceptions: Union[Type[_T], Tuple[Type[_T]]] = Exception,
                 ignore_exceptions: Union[Type[_T], Tuple[Type[_T]], None] = None,
                 log_enable: bool = True,
                 ever_fail_level: Literal['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'WARNING',
                 fail_level: Literal['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'ERROR'):
        super().__init__(max_attempts, delay, allow_exceptions, ignore_exceptions, log_enable, ever_fail_level,
                         fail_level)

    def retry(self, func):
        """重试装饰器
        使用方式:
            retry = Retry(...)

            @retry.retry
            def xxx(*args, **kwargs):
                # 业务逻辑
        Args:
            func: 需要重试的函数
        """

        def wrapper(*args, **kwargs):
            return self.do(func, *args, **kwargs)

        return wrapper

    def do(self, func, *args, **kwargs):
        """重试函数，重复执行指定的函数，直到达到最大重试次数或者函数执行成功为止。

        Args:
            func: 要执行的函数。
            args: 执行函数的参数
            kwargs: 执行函数的参数

        Returns:
            函数执行成功时返回函数的返回值，否则返回 None。
        """
        for attempt in range(1, self._max_attempts + 1):
            try:
                result = func(*args, **kwargs)
                return result  # 函数执行成功，直接返回结果
            except self._allow_exceptions as e:
                super()._handle_attempt_error(attempt, func, e, *args, **kwargs)


class AsyncRetry(_BaseRetry):
    """重试工具Async"""

    def __init__(self, max_attempts=3, delay=1,
                 allow_exceptions: Union[Type[_T], Tuple[Type[_T]]] = Exception,
                 ignore_exceptions: Union[Type[_T], Tuple[Type[_T]], None] = None,
                 log_enable: bool = True,
                 ever_fail_level: Literal['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'WARNING',
                 fail_level: Literal['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'ERROR'):
        super().__init__(max_attempts, delay, allow_exceptions, ignore_exceptions, log_enable, ever_fail_level,
                         fail_level)

    def retry(self, async_func):
        """重试装饰器
        使用方式:
            retry = AsyncRetry(...)

            @retry.retry
            async def xxx(*args, **kwargs):
                # 业务逻辑
        Args:
            async_func: 需要重试的async函数
        """

        async def wrapper(*args, **kwargs):
            return await self.do(async_func, *args, **kwargs)

        return wrapper

    async def do(self, async_func, *args, **kwargs):
        """重试函数，重复执行指定的函数，直到达到最大重试次数或者函数执行成功为止。

        Args:
            async_func: 要执行的async函数。
            args: 执行函数的参数
            kwargs: 执行函数的参数

        Returns:
            函数执行成功时返回函数的返回值，否则返回 None。
        """
        for attempt in range(1, self._max_attempts + 1):
            try:
                result = await async_func(*args, **kwargs)
                return result  # 函数执行成功，直接返回结果
            except self._allow_exceptions as e:
                super()._handle_attempt_error(attempt, async_func, e, *args, **kwargs)
