from seatools.ioc.config import cfg
from seatools.ioc.injects import Bean
from seatools.sqlalchemy.utils import new_client
from seatools.utils.dict_utils import deep_update
from loguru import logger
from seatools.sqlalchemy.dbconfig import CommonDBConfig


@Bean
def init_db_beans():
    if 'db' not in cfg():
        logger.warning('配置不存在[db]属性, 无法自动初始化数据库bean实例')
        return
    db_config = cfg()['db']
    if not isinstance(db_config, dict):
        logger.error('配置[db]属性不是字典类型, 无法自动初始化数据库bean实例')
        exit(1)
    for name, v in db_config.items():
        try:
            config = CommonDBConfig(**v)
            sqlalchemy_config = cfg().get('sqlalchemy')
            if config.sqlalchemy:
                if not sqlalchemy_config:
                    sqlalchemy_config = config.sqlalchemy
                else:
                    sqlalchemy_config = deep_update(sqlalchemy_config, config.sqlalchemy)
            client = new_client(config, config=sqlalchemy_config)
            # 注册bean
            Bean(name=config.name or name, primary=config.primary)(client)
        except Exception as e:
            logger.error(f'配置[db.{name}]存在不支持的参数, 请检查修改配置后重试')
            exit(1)

