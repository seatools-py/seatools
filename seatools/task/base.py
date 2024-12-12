import datetime
import uuid
from abc import ABC, abstractmethod
from typing import Any
from seatools.logger import PrefixLogger


class Task(ABC):
    """任务抽象类封装, 建议任务类业务统一继承该类"""

    def __init__(self):
        self._task_id = self._gen_task_id()
        self._logger = PrefixLogger(self._prefix())

    def run(self, *args, **kwargs) -> Any:
        """任务执行方法"""
        now = datetime.datetime.now()
        self._logger.info('开始处理, 任务参数: args: {}, kwargs: {}', args, kwargs)
        try:
            ans = self._run(*args, **kwargs)
            self._logger.success('处理完成, 本次任务执行耗时: {}, 返回值: {}, 任务参数: args: {}, kwargs: {}, 任务结果: {}',
                            (datetime.datetime.now() - now).total_seconds(), ans, args, kwargs, ans)
            return ans
        except Exception as e:
            self._logger.error('出错, 本次任务执行耗时: {}, 任务参数: args: {}, kwargs: {}, 异常信息: {}',
                               (datetime.datetime.now() - now).total_seconds(), args, kwargs, e)
            raise e

    def _prefix(self):
        return f'{self._task_name()}[{self._task_id}]'

    @abstractmethod
    def _run(self, *args, **kwargs) -> Any:
        """任务逻辑, 子类实现该方法来实现任务逻辑

        Args:
            args: 任务参数
            kwargs: 任务参数
        """
        raise NotImplementedError

    @abstractmethod
    def _task_name(self) -> str:
        """任务名称, 子类必须实现该方法

        Returns:
            任务名称
        """
        raise NotImplementedError

    def _gen_task_id(self):
        return str(uuid.uuid4())


class AsyncTask(ABC):
    """Async任务抽象类封装, 建议任务类业务统一继承该类"""

    def __init__(self):
        self._task_id = self._gen_task_id()
        self._logger = PrefixLogger(self._prefix())

    def _prefix(self):
        return f'{self._task_name()}[{self._task_id}]'

    @abstractmethod
    def _task_name(self) -> str:
        """任务名称, 子类必须实现该方法

        Returns:
            任务名称
        """
        raise NotImplementedError

    def _gen_task_id(self):
        return str(uuid.uuid4())

    async def run(self, *args, **kwargs) -> Any:
        """任务执行方法"""
        now = datetime.datetime.now()
        self._logger.info('开始处理, 任务参数: args: {}, kwargs: {}', args, kwargs)
        try:
            ans = await self._run(*args, **kwargs)
            self._logger.success('处理完成, 本次任务执行耗时: {}, 返回值: {}, 任务参数: args: {}, kwargs: {}, 任务结果: {}',
                              (datetime.datetime.now() - now).total_seconds(), ans, args, kwargs, ans)
            return ans
        except Exception as e:
            self._logger.error('出错, 本次任务执行耗时: {}, 任务参数: args: {}, kwargs: {}',
                               (datetime.datetime.now() - now).total_seconds(), args, kwargs)
            raise e

    @abstractmethod
    async def _run(self, *args, **kwargs) -> Any:
        """任务逻辑, 子类实现该方法来实现任务逻辑

        Args:
            args: 任务参数
            kwargs: 任务参数
        """
        raise NotImplementedError
