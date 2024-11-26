import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

from seatools.logger import get_loguru_adapter_logging_formatter


def setup_logging(file_name: str,
                  logger_name: str,
                  rotation_type: str = 'd',
                  rotation: int = 1,
                  serialize: bool = True,
                  retention_count: int = 3,
                  level: str = 'INFO',
                  extra: Optional[dict] = None):
    """设置logging日志记录, 与loguru相同的日志格式.

    Args:
        file_name: 日志文件路径及名称
        logger_name: 日志名称
        rotation:
        rotation_type:
        serialize: 是否序列化, 仅为True时生效
        retention_count:
        level: 日志级别
        extra: 额外信息
    """
    # 开启序列化则注入
    if serialize:
        # 增加一个适配loguru序列化的日志格式化器
        formatter_cls = get_loguru_adapter_logging_formatter()
        # 增加一个文件handler
        file_handler = TimedRotatingFileHandler(
            filename=file_name,
            when=rotation_type,
            interval=rotation,
            backupCount=retention_count,
            encoding='utf-8',
        )

        file_handler.setFormatter(formatter_cls('%(message)s', extra=extra))
        file_handler.addFilter(lambda e: e.levelno >= logging._nameToLevel[level])
        logging_logger = logging.getLogger(logger_name)
        logging_logger.addHandler(file_handler)
