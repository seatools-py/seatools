from .base import CommonDBConfig
from typing import Optional


class PostgresqlConfig(CommonDBConfig):
    """postgresql 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 5432
    user: Optional[str] = 'root'
    driver: Optional[str] = 'postgresql+psycopg2'


class AsyncPostgresqlConfig(CommonDBConfig):
    """postgresql async配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 5432
    user: Optional[str] = 'root'
    driver: Optional[str] = 'postgresql+asyncpg'
    is_async: Optional[bool] = True
