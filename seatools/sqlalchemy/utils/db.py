from typing import Union, TypeVar, Optional
from seatools.sqlalchemy import SqlAlchemyClient, AsyncSqlAlchemyClient
from seatools.sqlalchemy.dbconfig import CommonDBConfig, SqlalchemyConfig
from sqlalchemy import URL
from loguru import logger

__db_map = {}
REDIS_TYPE = TypeVar('REDIS_TYPE', bound='redis.Redis')
_DEFAULT_SQLALCHEMY_CONFIG = SqlalchemyConfig(echo=True, pool_recycle=3600)


def new_client(_id: CommonDBConfig, config: Optional[SqlalchemyConfig] = None) -> Union[SqlAlchemyClient, AsyncSqlAlchemyClient, REDIS_TYPE]:
    """DB客户端创建工具, 可通过通用DB配置对象创建 SqlAlchemyClient, AsyncSqlAlchemyClient, redis.Redis 实例.

    Args:
        _id: CommonDBConfig 对象
        config: sqlalchemy配置, redis暂不支持

    Returns:
        SqlAlchemyClient|AsyncSqlAlchemyClient: DB客户端, 根    据配置的is_async决定返回同步还是异步客户端
        redis.Redis: redis客户端, 根据配置生成

    """
    db_config, _id = _id, str(__gen_sqlalchemy_url(_id))
    client = __db_map.get(_id)
    if client:
        return client
    # 支持 redis 获取 redis.Redis 连接对象
    if db_config.orm_schema == 'redis':
        return __new_redis_client(db_config, _id)
    return __new_sqlalchemy_client(db_config, _id, config or _DEFAULT_SQLALCHEMY_CONFIG)


def __gen_sqlalchemy_url(config: CommonDBConfig):
    return URL.create(config.orm_schema,
                      host=config.host,
                      port=config.port,
                      username=config.user,
                      password=config.password,
                      database=config.db)


def __new_redis_client(config: CommonDBConfig, _id: str) -> REDIS_TYPE:
    try:
        # 优先使用redis-om
        from unique_tools.redis_om import get_redis_connection
        client = get_redis_connection(url=__gen_sqlalchemy_url(config).render_as_string(hide_password=False))
        __db_map[_id] = client
        return client
    except ImportError:
        import redis
        url = __gen_sqlalchemy_url(config).render_as_string(hide_password=False)
        client = redis.Redis.from_url(url, **{'decode_responses': True})
        __db_map[_id] = client
        return client



def __new_sqlalchemy_client(config: CommonDBConfig, _id: str, db_config: SqlalchemyConfig) -> Union[SqlAlchemyClient, AsyncSqlAlchemyClient]:
    url = __gen_sqlalchemy_url(config)
    logger.info('初始化ID[{}]的SqlAlchemyClient, 连接串[{}]', _id, url)
    client_cls = AsyncSqlAlchemyClient if config.is_async else SqlAlchemyClient
    # hive 需要额外处理
    if config.orm_schema == 'hive':
        try:
            from pyhive import hive
        except ImportError as e:
            logger.error('未安装pyhive依赖, sqlalchemy无法配置hive')
            raise e
        client = client_cls(url=url,
                            creator=lambda: hive.Connection(
                                host=config.host, port=config.port, username=config.user, database=config.db
                            ), **(db_config.model_dump(mode='json')))
    else:
        client = client_cls(url=url, **(db_config.model_dump(mode='json')))
    __db_map[_id] = client
    return client
