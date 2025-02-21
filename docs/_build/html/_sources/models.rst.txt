数据模型
========

基础模型
--------

提供了基于 pydantic 的基础模型支持:

.. code-block:: python

   from seatools.models import BaseModel

   class UserModel(BaseModel):
       id: int
       name: str
       age: int = None  # 可选字段

配置模型
--------

用于配置属性的模型装饰器:

.. code-block:: python

   from seatools.models import BaseModel
   from seatools.ioc import ConfigurationPropertiesBean

   @ConfigurationPropertiesBean(prop='mysql')
   class MysqlConfig(BaseModel):
       host: str
       port: int = 3306
       username: str
       password: str

通用响应
--------

.. code-block:: python

   from seatools.models import R

   # 成功响应
   response = R.ok(data=user)

   # 失败响应
   response = R.fail(msg="用户不存在")

分页模型
--------

.. code-block:: python

   from seatools.models import PageModel, PageR

   class UserPageRequest(PageModel):
       name: str = None

   page_response = PageR.ok(
       PageModel(rows=users, total=100)
   )
