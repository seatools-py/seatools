数据库支持
=========

SQLAlchemy 工具包
----------------

提供了 SQLAlchemy ORM 的便捷工具:

.. code-block:: python

   from seatools.sqlalchemy import SqlAlchemyClient
   from sqlalchemy import select

   client = SqlAlchemyClient(
       url='mysql+pymysql://user:pass@localhost/db',
       echo=True
   )

   # 使用 session
   with client.session() as session:
       users = session.execute(
           select(User).where(User.id == 1)
       ).scalars().all()

Redis-OM 扩展
------------

Redis-OM 的增强支持:

.. code-block:: python

   from seatools.redis_om import HashModel

   class User(HashModel):
       name: str
       age: int

Clickhouse 支持
--------------

Clickhouse 数据库支持:

.. code-block:: python

   from seatools.clickhouse.clickhouse_driver import ClickhouseDriverClient

   client = ClickhouseDriverClient(
       host='localhost',
       port=9000,
       database='default'
   )

   # 执行查询
   results = client.execute(
       'SELECT * FROM users WHERE id = %(id)s',
       {'id': 1}
   )
