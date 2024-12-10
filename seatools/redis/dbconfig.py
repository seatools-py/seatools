from typing import Optional

from seatools.ioc.database import DatabaseConfig


class RedisConfig(DatabaseConfig):
    """通用 DB 配置"""
    config: Optional[dict] = None
    driver: Optional[str] = 'redis'

