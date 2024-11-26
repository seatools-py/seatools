from typing import Optional

from loguru import logger
from seatools.logger import setup


def setup_loguru(file_name,
                 rotation="1 days",
                 serialize=True,
                 backtrace=True,
                 diagnose=False,
                 retention="3 days",
                 level='INFO',
                 extra: Optional[dict] = None):
    """设置loguru日志记录.

    Args:
        file_name: 日志文件路径及名称
        rotation:
        serialize: 是否序列化, 仅为True时生效
        backtrace:
        diagnose:
        retention:
        level: 日志级别
        extra: 额外信息
    """
    logger.configure(extra=extra)
    setup(file_name,
          rotation=rotation,
          serialize=serialize,
          backtrace=backtrace,
          diagnose=diagnose,
          retention=retention,
          level=level)
