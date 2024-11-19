from .base import CommonDBConfig
from typing import Optional


class RedisConfig(CommonDBConfig):
    """Redis 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 6379
    user: Optional[str] = ''
    orm_schema: Optional[str] = 'redis'
