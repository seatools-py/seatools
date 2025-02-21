IOC 容器详解
============

IOC 容器是 Seatools 的核心功能,提供依赖注入和控制反转能力。

Bean 管理
--------

使用 ``@Bean`` 装饰器来定义和管理 Bean。装饰器支持以下参数：

- name: bean 名称，不填则默认使用小写驼峰名称
- primary: 是否为该类型的默认 bean，默认为 False
- order: bean加载顺序，值越小越先加载，默认 0

.. code-block:: python

   from seatools.ioc import Bean, Autowired, run

   @Bean
   class UserService:
       def get_user(self):
           return "user"

   @Bean(name="orderService")
   class OrderService:
       def __init__(self, user_service: UserService):
           self.user_service = user_service

   Initialization
   ^^^^^^^^^^^^^

   Bean 的初始化有两种方式：

   1. 先执行 ``__post_construct__`` 方法
   2. 再执行 ``InitializingBean`` 的 ``after_properties_set`` 方法
   3. 如果同时存在，两个方法都会执行

   .. code-block:: python

       from seatools.beans.factory import InitializingBean

       @Bean
       class MyBean:
           def __post_construct__(self):
               # 初始化逻辑
               pass

       @Bean
       class MyOtherBean(InitializingBean):
           def after_properties_set(self):
               # 初始化逻辑
               pass

依赖注入
--------

使用 ``Autowired`` 进行依赖注入。注意事项:

- 只能在构造方法或普通方法的参数默认值中使用，不能用于类属性
- 使用 Autowired 时必须指定容器名称或容器类型
- 当类被 @Bean 装饰时，构造方法中的 Autowired 可以省略不写
- required 参数控制是否强制要求获取容器，默认为 True

.. code-block:: python

   from seatools.ioc import Autowired

   # 正确: 在被 @Bean 装饰的类中，构造方法参数可以省略 Autowired
   @Bean
   class PaymentService:
       def __init__(self, user_service: UserService, order_service: OrderService):
           self.user_service = user_service
           self.order_service = order_service

   # 如果类没有 @Bean 装饰，则必须显式使用 Autowired
   class NonBeanService:
       def __init__(self, user_service: UserService = Autowired(cls=UserService)):
           self.user_service = user_service

   # 正确: 在普通方法参数默认值中使用
   def process_order(order_id: int, user_service: UserService = Autowired(cls=UserService)):
       return user_service.get_user()

   # 也可以通过名称注入
   def process_order2(order_id: int, user_service = Autowired('userService')):
       return user_service.get_user()

   # 错误: 不能在类属性中使用
   class WrongUsage:
       # 这样使用是错误的!
       user_service: UserService = Autowired(cls=UserService)  # 即使指定类型也是错误的!

配置管理
--------

支持多种配置格式,默认使用 YAML:

.. code-block:: yaml

   # application.yml
   mysql:
     host: localhost
     port: 3306
     username: root

.. code-block:: python

   from seatools.ioc import ConfigurationPropertiesBean

   @ConfigurationPropertiesBean(prop='mysql')
   class MysqlConfig(BaseModel):
       host: str
       port: int = 3306
