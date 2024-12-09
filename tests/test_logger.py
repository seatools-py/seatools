from loguru import logger as log
from seatools.logger import setup as stp, get_loguru_adapter_logging_formatter
from seatools.logger.setup import setup_logging, setup_loguru, setup_uvicorn, setup_sqlalchemy
import logging

stp('test_logger.log')


@log.catch
def error_fun():
    return 1 / 0


def test_log_catch():
    f = error_fun()
    print(f)


def test_logging():
    filer_handler = logging.FileHandler('tmp/demo.log', encoding='utf-8')
    filer_handler.setLevel(logging.DEBUG)
    filer_handler.setFormatter(get_loguru_adapter_logging_formatter()())

    logger = logging.getLogger('a')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(filer_handler)

    logger.info("""啦啦啦
    \n\n
    """)


def test_logger_setup():
    setup_logging('./tmp/test_logging.log', logger_name='xxx')
    setup_sqlalchemy('./tmp/test_sqlalchemy.log')
    setup_uvicorn('./tmp/test_uvicorn.log')
    setup_loguru('./tmp/test_loguru.log')
