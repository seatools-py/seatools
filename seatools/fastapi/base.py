import warnings

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from seatools.models import R
from loguru import logger


def wrapper_exception_handler(app: FastAPI) -> FastAPI:
    """给FastAPI对象增加通用异常处理

    Args:
          app: fastapi 应用程序对象
    Returns:
        fastapi 应用程序对象, 封装部分异常处理
    """
    warnings.warn(
        '该工具包将废弃该方法, 请使用项目模板[https://gitee.com/dragons96/dragons96-cookiecutter-pystarter]生成模板内容',
        DeprecationWarning)

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request, exc: RequestValidationError):
        logger.error('发生请求参数校验异常, {}', exc)
        return PlainTextResponse(R.fail(msg='参数校验不通过', code=400).model_dump_json())

    @app.exception_handler(AssertionError)
    async def assert_exception_handler(request, exc):
        logger.error('发生断言异常, {}', exc)
        return PlainTextResponse(R.fail(msg=str(exc)).model_dump_json())

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        logger.error('发生http异常, {}', exc)
        return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

    @app.exception_handler(404)
    async def exception_404_handler(request, exc):
        logger.error('[404]请求不存在的路径, {}', request.url.path)
        return PlainTextResponse(R.fail(msg='资源不存在', code=404).model_dump_json())

    @app.exception_handler(Exception)
    async def exception_handler(request, exc):
        logger.error('发生未知异常, {}', exc)
        return PlainTextResponse(R.fail(msg='内部服务器错误').model_dump_json())

    return app
