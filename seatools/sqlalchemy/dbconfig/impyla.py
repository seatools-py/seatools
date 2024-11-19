from .base import CommonDBConfig
from typing import Optional


class ImpylaConfig(CommonDBConfig):
    """Impala 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 21050
    orm_schema: Optional[str] = 'impala'
