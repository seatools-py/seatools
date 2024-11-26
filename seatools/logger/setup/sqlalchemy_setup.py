from typing import Optional

from .logging_setup import setup_logging


def setup_sqlalchemy(file_name,
                     rotation_type: str = 'd',
                     rotation: int = 1,
                     serialize: bool = True,
                     retention_count: int = 3,
                     level: str = 'INFO',
                     extra: Optional[dict] = None):
    """设置sqlalchemy日志记录, 与loguru相同的日志格式."""
    setup_logging(file_name=file_name,
                  logger_name='sqlalchemy',
                  rotation_type=rotation_type,
                  rotation=rotation,
                  serialize=serialize,
                  retention_count=retention_count,
                  level=level,
                  extra=extra)
