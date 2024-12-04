from .base import CommonDBConfig
from typing import Optional


class SqliteConfig(CommonDBConfig):
    """Sqlite 配置"""
    driver: Optional[str] = 'sqlite'


class AsyncSqliteConfig(CommonDBConfig):
    """Sqlite async配置"""
    driver: Optional[str] = 'sqlite+aiosqlite'
    is_async: Optional[bool] = True
