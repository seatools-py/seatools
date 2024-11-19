from .base import CommonDBConfig
from typing import Optional


class ClickhouseConfig(CommonDBConfig):
    """Clickhouse 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 8123
    user: Optional[str] = 'root'
    orm_schema: Optional[str] = 'clickhouse'
