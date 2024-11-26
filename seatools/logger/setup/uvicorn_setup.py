from typing import Optional

from seatools.logger import get_loguru_adapter_logging_formatter


def setup_uvicorn(file_name,
                  rotation_type: str = 'd',
                  rotation: int = 1,
                  serialize: bool = True,
                  retention_count: int = 3,
                  level: str = 'INFO',
                  extra: Optional[dict] = None):
    """设置uvicorn文件记录, 与loguru相同的日志格式.

    Args:
        file_name: 日志文件路径及名称
        rotation:
        rotation_type:
        serialize: 是否序列化, 仅为True时生效
        retention_count:
        level: 日志级别
        extra: 额外信息
    """
    from uvicorn.config import LOGGING_CONFIG
    # 修改默认日志格式
    LOGGING_CONFIG['formatters']['default'][
        'fmt'] = '%(asctime)s | %(levelname)-8s | %(module)s.%(funcName)s:%(lineno)d - %(message)s'
    LOGGING_CONFIG['formatters']['access'][
        'fmt'] = '%(asctime)s | %(levelname)-8s | %(module)s.%(funcName)s:%(lineno)d - %(client_addr)s - “%(request_line)s” - %(status_code)s'

    # 开启序列化则注入
    if serialize:
        # 增加一个适配loguru序列化的日志格式化器
        file_formatter = {
            "()": get_loguru_adapter_logging_formatter(),
            'fmt': '%(message)s',
            'extra': extra or {},
        }
        # 增加一个文件handler
        file_handler = {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file",
            "filename": file_name,
            "when": rotation_type,
            "interval": rotation,
            "backupCount": retention_count,
            'level': level,
            'encoding': 'utf-8'
        }
        # 注入
        LOGGING_CONFIG['formatters']['file'] = file_formatter
        LOGGING_CONFIG['handlers']['file'] = file_handler
        LOGGING_CONFIG['loggers']['uvicorn']['handlers'].append('file')
        LOGGING_CONFIG['loggers']['uvicorn.access']['handlers'].append('file')
