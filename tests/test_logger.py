from loguru import logger as log
from seatools.logger import setup as stp, get_loguru_adapter_logging_formatter
import logging

stp('test_logger.log')


@log.catch
def error_fun():
    return 1 / 0


def test_log_catch():
    f = error_fun()
    print(f)


def test_logging():
    filer_handler = logging.FileHandler('demo.log', encoding='utf-8')
    filer_handler.setLevel(logging.DEBUG)
    filer_handler.setFormatter(get_loguru_adapter_logging_formatter()())

    logger = logging.getLogger('a')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(filer_handler)

    logger.info("""啦啦啦
    什么鬼
    \n\n
    """)
