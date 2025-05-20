from typing import Optional

from seatools.ioc.database import DatabaseConfig


class RedisConfig(DatabaseConfig):
    """通用 DB 配置"""
    config: Optional[dict] = None
    is_async: Optional[bool] = False
    driver: Optional[str] = 'redis'

