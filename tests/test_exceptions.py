from seatools import exceptions
from loguru import logger


def ex(d: int):
    try:
        logger.info(1 / d)
    except Exception as e:
        logger.error('异常')
        raise e


def test_uncaught_exception():
    exceptions.do_uncaught_exceptions(ex, 1, uncaught_exceptions=ImportError)
    exceptions.do_uncaught_exceptions(ex, 0, uncaught_exceptions=ZeroDivisionError)
