from sqlalchemy import BigInteger, String, DateTime, select, update, delete
from sqlalchemy.orm import Mapped, mapped_column
from loguru import logger
from seatools.sqlalchemy import SqlAlchemyClient, Base, AsyncSqlAlchemyClient
import datetime
from seatools.models import BaseModel


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime)


class UserModel(BaseModel):
    id: int
    name: str
    create_time:datetime.datetime


def get_helper():
    return SqlAlchemyClient('sqlite:///tmp/example.db', echo=True)


def test_create_model():
    Base.metadata.create_all(bind=get_helper().engine())


def test_insert():
    u = UserModel(id=2, name='测试用户2', create_time=datetime.datetime.now(), lalala='hee')
    helper = get_helper()
    with helper.session() as session:
        session.add(User.from_model(u))


def test_query():
    helper = get_helper()
    with helper.session() as session:
        users = session.execute(select(User).where(User.id >= 1)).scalars().all()
        users = [user.to_model(UserModel) for user in users]
        logger.info(users)


def test_update():
    helper = get_helper()
    with helper.session() as session:
        session.execute(update(User).where(User.id == 1).values(name='测试用户啦啦啦'))


def test_delete():
    helper = get_helper()
    with helper.session() as session:
        session.execute(delete(User).where(User.id == 2))


async def test_async_engine():
    helper = AsyncSqlAlchemyClient('sqlite+aiosqlite:///tmp/example.db', echo=True)
    async with helper.session() as session:
        session.add(User(id=1, name='测试用户1', create_time=datetime.datetime.now()))
        users = (await session.execute(select(User).where(User.id >= 1))).scalars().all()
        logger.info(users)
