Seatools Python Framework
=========================

Seatools 是一个参考 Java Spring 设计的轻量级 Python 框架，为 Python 开发者提供类似 Spring 的开发体验。主要特性包括 IOC 容器管理、配置管理、starter 机制等。

安装
----

.. code-block:: shell

   pip install seatools --upgrade

核心功能
--------

- IOC 容器管理
- IOC 配置管理
- starter 机制简化开发
- aop 切面 (实验中)
- 便捷的 API (与 Java Spring 类似)

IOC 容器
--------

IOC 容器是 Seatools 的核心功能，提供依赖注入和控制反转能力：

1. 包扫描机制，自动注册和管理 Bean
2. 基于代理对象和懒加载的依赖注入
3. 支持配置属性自动装配
4. 支持多种配置格式 (YAML、JSON、Properties 等)

示例代码:

.. code-block:: python

   from seatools.ioc import run, Bean, Autowired

   @Bean
   class UserService:
       def get_user(self):
           return "user"

   # 启动 IOC
   run(scan_package_names='xxx', config_dir='config')

   # 获取服务
   user_service = Autowired(cls=UserService)

工具包
------

文件处理
^^^^^^^^

提供多种文件格式的读写支持:

- JSON
- YAML
- CSV
- XML
- INI/TOML
- Properties
- Excel

.. code-block:: python

   from seatools.files import DynamicDataFileLoader

   loader = DynamicDataFileLoader()
   data = loader.load("config.yaml")

数据模型
^^^^^^^^

基于 pydantic 的模型支持:

- BaseModel 扩展
- 通用响应封装 (R)
- 分页模型

加密工具
^^^^^^^^

提供常用的加密算法:

- MD5
- Base16/32/64/85
- HMAC (MD5/SHA1/SHA256 等)

通知服务
^^^^^^^^

支持多种通知方式:

- SMTP 邮件
- 飞书机器人
- 支持富文本、卡片等多种消息格式

数据库支持
^^^^^^^^^^

- SQLAlchemy 工具包
- Redis-OM 扩展
- Clickhouse 驱动

其他工具
^^^^^^^^

- 日志工具 (基于 loguru)
- 重试机制
- 缓存工具
- 环境管理
- 任务调度
- 浏览器自动化 (UC)

版本要求
--------

- Python >= 3.9

联系方式
--------

- QQ: 521274311
- Email: 521274311@qq.com

项目地址
--------

- GitHub: https://github.com/seatools-py/seatools
- Gitee: https://gitee.com/seatools-py/seatools

相关项目
--------

- Cookiecutter 模板: https://github.com/seatools-py/cookiecutter-seatools-python

更多文档
--------

.. toctree::
   :maxdepth: 2

   ioc
   files
   models
   notices
   database
   utils
   env
   best_practices
   builders
   retry
   cache
