from .base import CommonDBConfig
from typing import Optional


class MysqlConfig(CommonDBConfig):
    """Mysql 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 3306
    user: Optional[str] = 'root'
    orm_schema: Optional[str] = 'mysql+pymysql'


class AsyncMysqlConfig(CommonDBConfig):
    """Mysql async配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 3306
    user: Optional[str] = 'root'
    orm_schema: Optional[str] = 'mysql+aiomysql'
    is_async: Optional[bool] = True
