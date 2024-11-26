from typing import Optional

from seatools.models import BaseModel


class SqlalchemyConfig(BaseModel):
    """sqlalchemy相关配置"""
    echo: Optional[bool] = False
    # 连接池回收周期
    pool_recycle: Optional[int] = 3600


class CommonDBConfig(BaseModel):
    """通用 DB 配置"""
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    db: Optional[str] = None
    # sqlalchemy的schema, 仅使用sqlalchemy需要配置, 例如:sqlite, mysql+pymysql等等
    orm_schema: Optional[str] = None
    # 是否是async连接
    is_async: Optional[bool] = False
    # 是否是ioc primary实例
    primary: Optional[bool] = False
    sqlalchemy: Optional[dict] = None
