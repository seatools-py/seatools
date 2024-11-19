from .base import CommonDBConfig
from typing import Optional


class HiveConfig(CommonDBConfig):
    """Hive 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 10000
    orm_schema: Optional[str] = 'hive'
