最佳实践指南
=============

本文档提供使用 Seatools 框架的最佳实践建议。

项目结构
--------

推荐的项目目录结构:

.. code-block:: text

   my_project/
   ├── config/
   │   ├── application.yml         # 基础配置
   │   ├── application-dev.yml     # 开发环境配置
   │   ├── application-test.yml    # 测试环境配置
   │   └── application-pro.yml     # 生产环境配置
   ├── my_project/
   │   ├── __init__.py
   │   ├── models/                 # 数据模型
   │   │   ├── __init__.py
   │   │   └── user.py
   │   ├── services/              # 业务服务
   │   │   ├── __init__.py
   │   │   └── user_service.py
   │   ├── dao/                   # 数据访问
   │   │   ├── __init__.py
   │   │   └── user_dao.py
   │   └── utils/                 # 工具类
   │       ├── __init__.py
   │       └── common.py
   └── main.py                    # 程序入口

IOC 最佳实践
------------

1. Bean 定义
^^^^^^^^^^^^

- 单例 Bean 使用类装饰器
- 多例 Bean 使用函数装饰器
- Bean 名称使用小写字母+下划线

.. code-block:: python

   from seatools.ioc import Bean, Autowired

   # 单例
   @Bean
   class UserService:
       def get_user(self):
           return "user"

   # 多例
   @Bean(name="orderService")
   class OrderService:
       def __init__(self, user_service: UserService):
           self.user_service = user_service

2. 依赖注入
^^^^^^^^^^^

- 推荐使用构造函数注入
- Autowired 只能用于方法参数的默认值
- 不能在类属性中使用 Autowired
- 使用 Autowired 时必须指定容器名称或类型
- 被 @Bean 装饰的类的构造方法中可以省略 Autowired
- 使用类型注解提高代码可读性

.. code-block:: python

   @Bean
   class OrderService:
       def __init__(self, user_service: UserService):
           self.user_service = user_service

   def process_order(self, order_service: OrderService = Autowired(cls=OrderService)):
       return order_service.process()

   def process_order2(self, order_service = Autowired('orderService')):
       return order_service.process()

   # 没有 @Bean 装饰器，必须使用 Autowired
   class NonBeanService:
       def __init__(self, user_service: UserService = Autowired(cls=UserService)):
           self.user_service = user_service

数据库最佳实践
--------------

1. ORM 使用
^^^^^^^^^^^

- 业务层使用 pydantic 模型
- 数据访问层使用 SQLAlchemy 模型
- 使用 BaseMapper 简化 CRUD 操作

.. code-block:: python

   # 模型定义
   class UserModel(BaseModel):
       id: int
       name: str

   # ORM 模型
   class User(Base):
       __tablename__ = 'users'
       id = Column(Integer, primary_key=True)
       name = Column(String)

   # 数据访问层
   class UserDAO:
       def __init__(self, session):
           self.session = session

       def get(self, user_id):
           return self.session.query(User).get(user_id)

2. 事务管理
^^^^^^^^^^^

- 使用上下文管理器处理事务
- 合理设置事务边界
- 避免长事务

.. code-block:: python

   with client.session() as session:
       try:
           # 业务操作
           session.commit()
       except Exception:
           session.rollback()
           raise

配置管理最佳实践
----------------

1. 配置分层
^^^^^^^^^^^

- 按环境拆分配置文件
- 敏感信息使用环境变量
- 使用配置类封装配置项

.. code-block:: python

   @ConfigurationPropertiesBean(prop='mysql')
   class MysqlConfig(BaseModel):
       host: str
       port: int = 3306
       username: str
       password: str

2. 环境管理
^^^^^^^^^^^

- 使用 ENV 环境变量区分环境
- 避免在代码中硬编码环境判断
- 使用环境工具类获取环境

.. code-block:: python

   from seatools.env import get_env

   env = get_env()
   if env.is_dev():
       # 开发环境逻辑

日志最佳实践
------------

1. 日志配置
^^^^^^^^^^^

- 按日期滚动日志文件
- 设置合理的日志保留期
- 区分不同级别日志

.. code-block:: python

   setup(
       'app.log',
       rotation='1 days',    # 每天滚动
       retention='30 days',  # 保留30天
       backtrace=True,      # 异常时显示完整堆栈
       diagnose=False       # 生产环境关闭诊断
   )

2. 日志使用
^^^^^^^^^^^

- 合理使用日志级别
- 记录关键业务节点
- 包含必要的上下文信息

.. code-block:: python

   logger.info('处理订单 [orderId={}]', order_id)
   try:
       # 业务逻辑
   except Exception as e:
       logger.exception('订单处理失败 [orderId={}]', order_id)

安全最佳实践
------------

1. 密码处理
^^^^^^^^^^^

- 使用加盐哈希存储密码
- 避免明文传输密码
- 定期更新密钥

.. code-block:: python

   from seatools.cryptography import md5_hmac

   def hash_password(password: str, salt: str) -> str:
       return md5_hmac(salt, password)

2. 敏感信息
^^^^^^^^^^^

- 使用环境变量存储密钥
- 加密存储敏感配置
- 限制敏感信息访问范围

性能优化建议
------------

1. 缓存使用
^^^^^^^^^^^

- 合理使用缓存
- 设置适当的过期时间
- 及时清理无用缓存

.. code-block:: python

   @cache.cache(key='user-${user_id}', ttl=3600)
   def get_user(user_id: int):
       return user_dao.get(user_id)

2. 数据库优化
^^^^^^^^^^^^

- 使用连接池
- 避免 N+1 查询问题
- 合理使用批量操作

.. code-block:: python

   # 批量插入
   session.bulk_save_objects(objects)

   # 避免 N+1
   users = session.query(User).options(
       joinedload(User.orders)
   ).all()
