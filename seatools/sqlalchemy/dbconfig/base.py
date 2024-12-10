from typing import Optional

from seatools.models import BaseModel
from seatools.ioc.database.dbconfig import DatabaseConfig


class SqlalchemyConfig(BaseModel):
    """sqlalchemy相关配置"""
    echo: Optional[bool] = False
    # 连接池回收周期
    pool_recycle: Optional[int] = 3600


class CommonDBConfig(DatabaseConfig):
    """通用 DB 配置"""
    db: Optional[str] = None
    # 是否是async连接
    is_async: Optional[bool] = False
    sqlalchemy: Optional[dict] = None
