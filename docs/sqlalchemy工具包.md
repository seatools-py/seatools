### `seatools.sqlalchemy` sqlalchemy ORM工具包
1. `seatools.sqlalchemy.Base` - `class`: sqlalchemy模型基础类, 所有sqlalchemy的模型均应该继承该类
2. `seatools.sqlalchemy.SqlAlchemyHelper` - `class`: sqlalchemy客户端工具类, 使用示例如下:

```python
from seatools.sqlalchemy import SqlAlchemyClient, Base, AsyncSqlAlchemyClient
from seatools.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, select, update, delete
from typing import Optional


class User(Base):
    id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class AddUserModel(BaseModel):
    name: str


class UserModel(BaseModel):
    id: int
    name: str


# 同步
client = SqlAlchemyClient(url='sqlite:///test.db',
                          echo=True,  # 打印sql
                          )
with client.session() as session:
    # 新增
    session.add(User.from_model(AddUserModel(name='测试用户1')))
    # 查询 [User(...)]
    users = session.execute(select(User).where(User.id == 1)).scalars().all()
    # 查询 User, 基于ID
    user = session.execute(select(User).where(User.id == 1)).scalars().one()
    # sqlalchemy model转pydantic model
    user_model = user.to_model(UserModel)
    # 修改
    session.execute(update(User).where(User.id == 1).values(name='测试用户-修改'))
    # 删除
    session.execute(delete(User).where(User.id == 1))


# asyncio
async def run_async():
    client = AsyncSqlAlchemyClient(url='sqlite+aiosqlite:///test.db',
                                   echo=True,  # 打印sql
                                   )
    async with client.session() as session:
        session.add(User.from_model(AddUserModel(name='测试用户1')))
        # 查询 User, 基于ID
        user = (await session.execute(select(User).where(User.id == 1))).scalars().one()
        # sqlalchemy model转pydantic model
        user_model = user.to_model(UserModel)
        # 修改
        await session.execute(update(User).where(User.id == 1).values(name='测试用户-修改'))
        # 删除
        await session.execute(delete(User).where(User.id == 1))

```
PS: 推荐仅在DAO层使用sqlalchemy的Model, 在业务层仅用pydantic的model
