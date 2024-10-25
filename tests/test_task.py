from typing import Any

from seatools.task import Task, AsyncTask


class TestTask(Task):

    def _run(self, *args, **kwargs) -> Any:
        for i in range(1000):
            self._logger.info('输出: {}', i)

    def _task_name(self) -> str:
        return "测试任务"


class TestAsyncTask(AsyncTask):

    async def _run(self, *args, **kwargs) -> Any:
        for i in range(1000):
            self._logger.info('输出: {}', i)

    def _task_name(self) -> str:
        return "测试async任务"


def test_task():
    task = TestTask()
    task.run()


def test_async_task():
    import asyncio
    task = TestAsyncTask()
    asyncio.run(task.run())
