import logging
import time
import traceback
import datetime
import json
from typing import Optional


class LoguruSerializeAdapterFormatter(logging.Formatter):

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, extra: Optional[dict] = None):
        super().__init__(fmt, datefmt, style, validate)
        self._extra = extra


    def format(self, record):
        elapsed_seconds = time.time() - record.created
        elapsed_repr = self._format_elapsed(elapsed_seconds)
        exception_msg = self._format_line_break(traceback.format_exc()) if record.exc_info else ''
        message = self._format_line_break(record.getMessage())
        log_record = {
            "text": message + f"\n{exception_msg}",
            "record": {
                "elapsed": {
                    "repr": elapsed_repr,
                    "seconds": elapsed_seconds
                },
                "exception": self._format_exception(record.exc_info),
                "extra": self._extra or {},
                "file": {
                    "name": record.filename,
                    "path": record.pathname
                },
                "function": record.funcName,
                "level": {
                    "icon": self._get_level_icon(record.levelname),
                    "name": record.levelname,
                    "no": record.levelno
                },
                "line": record.lineno,
                "message": message,
                "module": record.module,
                "name": record.name,
                "process": {
                    "id": record.process,
                    "name": record.processName
                },
                "thread": {
                    "id": record.thread,
                    "name": record.threadName
                },
                "time": {
                    "repr": datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f%z'),
                    "timestamp": record.created
                }
            }
        }
        return json.dumps(log_record, ensure_ascii=False)

    @staticmethod
    def _get_level_icon(level_name: str):
        if level_name == 'TRACE':
            return '✏️'
        if level_name == 'DEBUG':
            return '🐞'
        elif level_name == 'INFO':
            return 'ℹ️'
        elif level_name == 'WARNING':
            return '⚠️'
        elif level_name == 'ERROR':
            return '❌'
        elif level_name == 'CRITICAL':
            return '☠️'
        return ''

    @staticmethod
    def _format_elapsed(elapsed_seconds):
        hours, remainder = divmod(elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:0>2}:{:0>2}:{:0>2}.{:06}".format(int(hours), int(minutes), int(seconds),
                                                   int((elapsed_seconds - int(elapsed_seconds)) * 1000000))

    def _format_exception(self, exc_info):
        if exc_info:
            exc_type, exc_value, exc_traceback = exc_info
            return {
                "type": exc_type.__name__,
                "message": self._format_line_break(str(exc_value)),
                "traceback": True
            }
        else:
            return None

    @staticmethod
    def _format_line_break(text: str) -> str:
        # return text.replace('\r', '\\r').replace('\n', '\\n')
        return text


def get_loguru_adapter_logging_formatter():
    """获取适配loguru serialize格式的logging.Formatter类型

    Returns:
        返回logging.Formatter类
    """
    return LoguruSerializeAdapterFormatter
