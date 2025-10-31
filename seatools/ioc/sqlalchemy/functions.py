import asyncio
import functools
import uuid
from typing import Optional
import inspect
from contextvars import ContextVar

from seatools.utils import list_utils
from seatools.ioc.injects import Autowired
from seatools.sqlalchemy import SqlAlchemyClient, AsyncSqlAlchemyClient

__db_context_id = ContextVar('sqlalchemy_context_id')
__db_session_map = {}


def auto_session(*args, db: Optional[str] = None, field_name: Optional[str] = 'session',
                 autocommit: bool = True,
                 **kw):
    """自动注入Session/AsyncSession装饰器, 通过ContextVar保证上下文的Session/AsyncSession一致性

    使用方法:
        ```python
            @auto_session('xxx') # 若仅存在一个db 或者使用某个primary=True的db, 可简写为 @auto_session() 或 @auto_session
            [async] def handle1(*args, session: Union[Session, AsyncSession] = None, **kwargs):
                [await] session.execute(...)
                [await] handle2(...)

            @auto_session('xxx')
            [async] def handle2(*args, session: Union[Session, AsyncSession] = None, **kwargs):
                [await] session.execute(...)

            # 执行
            handle1() # asyncio.run(handle1())
        ```
        session 由装饰器管理自动注入无需传参, 传参则使用传递的session。
        上述示例 handle1 与 handle2 相同db共用同一个session, 保障连续调用的事务一致性, 全部执行完成自动执行commit, 失败则自动执行rollback

    Args:
        db: 数据库配置, 与 Autowired 使用一致填写bean名称, 当只有一个db配置或者有注入primary的db bean时可不传该参数获取session实例
        field_name: 需要注入Session/AsyncSession的字段
        autocommit: Session.autocommit
        kw: 额外的Session参数配置
    """

    def init_sqlalchemy_context_id():
        try:
            __db_context_id.get()
        except LookupError:
            context_id = uuid.uuid4()
            __db_context_id.set(context_id)

    async def do_async_func(func, *args, _inner_extra, **kwargs):
        context_id = __db_context_id.get()
        if __db_session_map.get(context_id) is None:
            __db_session_map[context_id] = {}
        __db_session_map[context_id][db] = _inner_extra["session"]
        kwargs[field_name] = _inner_extra["session"]
        ans = await func(*args, **kwargs)
        if context_id in __db_session_map and db in __db_session_map[context_id]:
            del __db_session_map[context_id][db]
        if context_id in __db_session_map and len(__db_session_map[context_id]) == 0:
            del __db_session_map[context_id]
        return ans

    def do_func(func, *args, _inner_extra, **kwargs):
        context_id = __db_context_id.get()
        if __db_session_map.get(context_id) is None:
            __db_session_map[context_id] = {}
        __db_session_map[context_id][db] = _inner_extra["session"]
        kwargs[field_name] = _inner_extra["session"]
        ans = func(*args, **kwargs)
        if context_id in __db_session_map and db in __db_session_map[context_id]:
            del __db_session_map[context_id][db]
        if context_id in __db_session_map and len(__db_session_map[context_id]) == 0:
            del __db_session_map[context_id]
        return ans

    def wrapper(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if kwargs.get(field_name):
                return await func(*args, **kwargs)
            init_sqlalchemy_context_id()
            session_dict = __db_session_map.get(__db_context_id.get())
            if session_dict and session_dict.get(db):
                kwargs[field_name] = session_dict[db]
                return await func(*args, **kwargs)
            cli = Autowired(db, cls=AsyncSqlAlchemyClient, required=False)
            # 检查是否存在bean实例
            if cli.ioc_bean():
                async with cli.session(
                    autocommit=autocommit,
                    **kw,
                ) as session:
                    return await do_async_func(func, _inner_extra=dict(session=session), *args, **kwargs)
            cli = Autowired(db, cls=SqlAlchemyClient)
            with cli.session(
                autocommit=autocommit,
                **kw,
            ) as session:
                return await do_async_func(func, _inner_extra=dict(session=session), *args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            if kwargs.get(field_name):
                return func(*args, **kwargs)
            init_sqlalchemy_context_id()
            session_dict = __db_session_map.get(__db_context_id.get())
            if session_dict and session_dict.get(db):
                kwargs[field_name] = session_dict[db]
                return func(*args, **kwargs)
            cli = Autowired(db, cls=SqlAlchemyClient)
            with cli.session(
                autocommit=autocommit,
                **kw,
            ) as session:
                return do_func(func, _inner_extra=dict(session=session), *args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    if len(args) == 1 and (inspect.isclass(args[0]) or inspect.isfunction(args[0])):
        return wrapper(args[0])

    db = list_utils.get(args, 0, db)
    field_name = list_utils.get(args, 1, field_name)
    autocommit = list_utils.get(args, 2, autocommit)

    return wrapper


def new_session(*args, db: Optional[str] = None, field_name: Optional[str] = 'session',
                autocommit: bool = True,
                **kw):
    """自动注入Session/AsyncSession装饰器, 仅新建一个Session/AsyncSession, 需要自己保障事务一致性

    使用方法:
        ```python
            @new_session('xxx') # 若仅有一个db或者使用primary=True的db则可简写 @new_session() 或 @new_session
            [async] def handle1(*args, session: Union[Session, AsyncSession] = None, **kwargs):
                [await] session.execute(...)
                [await] handle2(session=session)

            [async] def handle2(*args, session: Union[Session, AsyncSession] = None, **kwargs):
                [await] session.execute(...)

            # 执行
            handle1() # asyncio.run(handle1())
        ```
        session 由装饰器生成自动注入, 与auto_session相比不具备自动注入的传递性。
        执行完成自动执行commit, 失败则自动执行rollback
    Args:
        db: 数据库配置, 与 Autowired 使用一致填写bean名称, 当只有一个db配置或者有注入primary的db bean时可不传该参数获取session实例
        field_name: 需要注入Session/AsyncSession的字段
        autocommit: Session.autocommit
        kw: Session额外参数
    """
    def wrapper(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if kwargs.get(field_name):
                return await func(*args, **kwargs)
            cli = Autowired(db, cls=AsyncSqlAlchemyClient, required=False)
            if cli.ioc_bean():
                async with cli.session(
                    autocommit=autocommit,
                    **kw,
                ) as session:
                    kwargs[field_name] = session
                    return await func(*args, **kwargs)
            cli = Autowired(db, cls=SqlAlchemyClient)
            with cli.session(
                autocommit=autocommit,
                **kw,
            ) as session:
                kwargs[field_name] = session
                return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            if kwargs.get(field_name):
                return func(*args, **kwargs)
            cli = Autowired(db, cls=SqlAlchemyClient)
            with cli.session(
                autocommit=autocommit,
                **kw,
            ) as session:
                kwargs[field_name] = session
                return func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    if len(args) == 1 and (inspect.isclass(args[0]) or inspect.isfunction(args[0])):
        return wrapper(args[0])

    db = list_utils.get(args, 0, db)
    field_name = list_utils.get(args, 1, field_name)
    autocommit = list_utils.get(args, 2, autocommit)

    return wrapper
