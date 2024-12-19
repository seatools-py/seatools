from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from contextlib import contextmanager, asynccontextmanager
from typing import Any, Type, TypeVar
from pydantic import BaseModel

_T = TypeVar('_T', bound='BaseModel')
_BASE = TypeVar('_BASE', bound='Base')


class Base(DeclarativeBase):
    """orm model 基础类"""

    def to_dict(self, exclude_none: bool = False, exclude_zero: bool = False) -> dict:
        """将当前model转为dict对象

        Args:
            exclude_none: 忽略为none的字段
            exclude_zero: 忽略0值的字段, 包含'', 0, False等0值
        """
        ans = {}
        for col in self.__table__.columns:
            val = getattr(self, col.name)
            if val or not exclude_none and not exclude_zero:
                ans[col.name] = val
            elif exclude_none and val is not None:
                ans[col.name] = val
        return ans

    def to_model(self, modelclass: Type[BaseModel], exclude_none: bool = False, exclude_zero: bool = False, **kw) -> _T:
        """将当前model转为pydantic的model对象

        Args:
            modelclass: 具体的模型类型
            exclude_none: 忽略为none的字段
            exclude_zero: 忽略0值的字段, 包含'', 0, False等0值
            kw: 自定义映射
        """
        model_dict = self.to_dict(exclude_none=exclude_none, exclude_zero=exclude_zero)
        for k, v in model_dict.items():
            kw.setdefault(k, v)
        return modelclass(**kw)

    @classmethod
    def from_model(cls,
                   model: BaseModel,
                   ignore_absent_fields: bool = True,
                   include: Any = None,
                   exclude: Any = None,
                   by_alias: bool = False,
                   exclude_unset: bool = False,
                   exclude_defaults: bool = False,
                   exclude_none: bool = False,
                   round_trip: bool = False,
                   ) -> _BASE:
        """将pydantic的model转为当前类型model

        Args:
            model: pydantic的模型值
            ignore_absent_fields: 忽略当前model中不存在的pydantic model的属性
            include: A list of fields to include in the output.
            exclude: A list of fields to exclude from the output.
            by_alias: Whether to use the field's alias in the dictionary key if defined.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of `None`.
            round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
        """
        model_dict = model.model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip
        )
        if ignore_absent_fields:
            for key in list(model_dict.keys()):
                if not hasattr(cls, key):
                    del model_dict[key]
        return cls(**model_dict)

    @classmethod
    def truncate(cls, session: Session):
        """Truncate sql."""
        return session.execute(text('TRUNCATE {}'.format(cls.__tablename__)))


class SqlAlchemyClient:
    """SqlAlchemy工具客户端"""

    def __init__(self, url: str, echo: bool = False,
                 session_cls = Session,
                 **kwargs: Any):
        """创建sqlalchemy工具客户端

        Args:
            url: 连接串
                示例:
                    sqlite:///dbname
                    mysql+pymysql://username:password@host:port/dbname
            echo: The echo=True parameter indicates that SQL emitted by connections will be logged to standard out.
        """
        self._engine = create_engine(url, echo=echo, **kwargs)
        self._session_maker = sessionmaker(bind=self._engine, expire_on_commit=False, class_=session_cls)

    @contextmanager
    def session(self, **kw) -> Session:
        """获取session上下文对象

        使用示例:
            client = SqlAlchemyClient('xxxx')
            with client.session() as session:
                session.execute()
                session.get()
        """
        session = self._session_maker(**kw)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if session:
                session.close()

    def engine(self) -> Engine:
        """获取引擎"""
        return self._engine


class AsyncSqlAlchemyClient:
    """SqlAlchemy异步工具客户端"""

    def __init__(self, url: str, echo: bool = False,
                 session_cls = AsyncSession,
                 **kwargs: Any):
        """创建sqlalchemy异步工具客户端

        Args:
            url: 连接串
            示例:
                sqlite:///dbname
                mysql+pymysql://username:password@host:port/dbname
            echo: The echo=True parameter indicates that SQL emitted by connections will be logged to standard out.
        """
        self._engine = create_async_engine(url, echo=echo, **kwargs)
        self._session_maker = async_sessionmaker(bind=self._engine, expire_on_commit=False, class_=session_cls)

    @asynccontextmanager
    async def session(self, **kw) -> AsyncSession:
        """获取session上下文对象

        使用示例:
            client = AsyncSqlAlchemyClient('xxxx')
            with client.session() as session:
                session.execute()
                session.get()
        """
        session = self._session_maker(**kw)
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            if session:
                await session.close()

    def engine(self) -> AsyncEngine:
        """获取引擎"""
        return self._engine
