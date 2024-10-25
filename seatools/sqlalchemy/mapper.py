from typing import TypeVar, Optional, List, Union, Any, Type, Sequence, Literal, Dict

from sqlalchemy import select, ColumnElement, update, Select, Result, func, BinaryExpression, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.engine import ScalarResult
from sqlalchemy.sql.elements import SQLCoreOperations

_BASE = TypeVar('_BASE', bound='Base')
_SQLSelectOperations = Union[Type[_BASE], SQLCoreOperations[_BASE], BinaryExpression, List[BinaryExpression], List[SQLCoreOperations[_BASE]]]
_SQLCondOperations = Union[SQLCoreOperations[_BASE], bool]  # !注意, 不能传递bool类型, 仅为了兼容编译器解析问题
_SQLOrderOperations = Union[SQLCoreOperations[_BASE], ColumnElement[_BASE]]
_SQLGroupOperations = Union[SQLCoreOperations[_BASE], ColumnElement[_BASE]]
_SQLHavingOperations = Union[SQLCoreOperations[_BASE], ColumnElement[_BASE]]


def _wrapper_to_list(item: Union[List[Any], Any]):
    if isinstance(item, list):
        return item
    return [item]


def _gen_model_query_select(entities: _SQLSelectOperations,
                            conds: Optional[Union[List[_SQLCondOperations], _SQLCondOperations]] = None,
                            orders: Optional[Union[List[_SQLOrderOperations], _SQLOrderOperations]] = None,
                            groups: Optional[Union[List[_SQLGroupOperations], _SQLGroupOperations]] = None,
                            group_conds: Optional[Union[List[_SQLHavingOperations], _SQLHavingOperations]] = None,
                            offset: Optional[int] = None,
                            limit: Optional[int] = None,
                            ) -> Select[_BASE]:
    q = select(*(_wrapper_to_list(entities)))
    if conds is not None:
        q = q.where(*(_wrapper_to_list(conds)))
    if orders is not None:
        q = q.order_by(*(_wrapper_to_list(orders)))
    if groups is not None:
        q = q.group_by(*(_wrapper_to_list(groups)))
    if group_conds is not None:
        q = q.having(*(_wrapper_to_list(group_conds)))
    if offset is not None:
        q = q.offset(offset)
    if limit is not None:
        q = q.limit(limit)
    return q


def _get_result(result: Result[_BASE],
                result_analysis: Literal[
                    'scalar', 'scalars', 'list', 'scalars-list', 'first', 'scalars-first', 'one_or_none', 'scalars-one_or_none', 'one', 'scalars-one', None] = 'scalars-list'):
    ans = result
    result_steps = result_analysis.split('-')
    for result_step in result_steps:
        if result_step == 'scalars':
            ans = ans.scalars()
        if result_step == 'list':
            ans = ans.all()
        if result_step == 'first':
            ans = ans.first()
        if result_step == 'scalar':
            ans = ans.scalar()
        if result_step == 'one_or_none':
            ans = ans.one_or_none()
        if result_step == 'one':
            ans = ans.one()
    return ans


class BaseMapper:
    """提供表的基础操作封装

    注意, 如果__tableclass__存在字段名称name与属性名称不一致, 则必须设置字段key参数且值内容与属性名称一致, 否则可能出现未知错误
    """

    # 表类型, 需要继承 DeclarativeBase
    __tableclass__: Type[_BASE] = None
    # 是否自动提交, 为True将会自动提交
    __autocommit__: bool = False

    def __init__(self):
        self._table = self.__tableclass__.__table__
        self._columns = []
        self._attr_column_map = {}
        self._primary_keys = []
        self._exclude_primary_columns = []
        for column in self._table.columns:
            self._columns.append(column.key)
            self._attr_column_map[column.key] = column.name
            if column.primary_key:
                self._primary_keys.append(column.key)
            else:
                self._exclude_primary_columns.append(column.key)

    def save(self, session: Session, instance: _BASE, ignore_none: bool = True) -> bool:
        """新增或修改

        Args:
            session: 数据库session
            instance: 实例对象
            ignore_none: 忽略None值, 为True时新增和删除将会忽略none字段
        """
        _type: Literal['add', 'update', None] = None
        # 按照所有主键查询是否存在
        conds = []
        for primary_key in self._primary_keys:
            conds.append(getattr(self.__tableclass__, primary_key) == getattr(instance, primary_key))
        # 查询, 存在则修改, 否则新增
        item = self.query(session, conds=conds, limit=1, result='scalars-first')
        if not item:
            session.add(instance)
            self._check_commit(session)
        else:
            if not conds:
                raise ValueError('表{}不存在主键, 无法通过该方法更新数据'.format(self.__tableclass__.__tablename__))
            sets = {}
            for attr_name in self._exclude_primary_columns:
                attr = getattr(instance, attr_name)
                if attr is not None or not ignore_none:
                    sets[attr_name] = attr
            if sets:
                self.update(session, sets=sets, conds=conds)
        return True

    def query_one(self, session: Session,
                  conds: Optional[Union[List[_SQLCondOperations], _SQLCondOperations]] = None,
                  orders: Optional[Union[List[_SQLOrderOperations], _SQLOrderOperations]] = None,
                  groups: Optional[Union[List[_SQLGroupOperations], _SQLGroupOperations]] = None,
                  group_conds: Optional[Union[List[_SQLHavingOperations], _SQLHavingOperations]] = None,
                  offset: Optional[int] = None,
                  limit: Optional[int] = None,
                  fields: Optional[_SQLSelectOperations] = None,
                  result: Literal[
                      'first', 'scalars-first', 'one_or_none', 'scalars-one_or_none', 'one', 'scalars-one', None] = 'scalars-first',
                  **kwargs) -> Union[ScalarResult[_BASE], Sequence[_BASE], _BASE, None, Any]:
        """条件查询, 仅返回单条记录, query的部分分支, 具体见query方法"""
        return self.query(session, conds, orders, groups, group_conds, offset, limit, fields, result, **kwargs)

    def query(self, session: Session,
              conds: Optional[Union[List[_SQLCondOperations], _SQLCondOperations]] = None,
              orders: Optional[Union[List[_SQLOrderOperations], _SQLOrderOperations]] = None,
              groups: Optional[Union[List[_SQLGroupOperations], _SQLGroupOperations]] = None,
              group_conds: Optional[Union[List[_SQLHavingOperations], _SQLHavingOperations]] = None,
              offset: Optional[int] = None,
              limit: Optional[int] = None,
              query: Optional[_SQLSelectOperations] = None,
              result: Literal[
                  'scalar', 'scalars', 'list', 'scalars-list', 'first', 'scalars-first', 'one_or_none', 'scalars-one_or_none', 'one', 'scalars-one', None] = 'scalars-list',
              **kwargs) -> Union[ScalarResult[_BASE], Sequence[_BASE], _BASE, None, Any]:
        """条件查询

        Args:
            session: 数据库session
            conds: 条件, 例如 XXXTable.id == 2, XXXTable.id.in_(1, 2, 3), 传递该形式的条件
            orders: 排序, 例如 XXXTable.id.asc(), XXXTable.id.desc() 传递该形式参数
            groups: 分组
            group_conds: 分组条件, 对应 sql having
            offset: offset
            limit: limit
            query: 查询内容, 为 None 默认查询表所有字段, 允许传数据表属性字段及列表, 允许传递sqlalchemy.func函数及函数列表
            result: 返回数据形式, 默认 scalars_list, 各类型见源码

        Returns:
            ScalarResult或者List
        """
        q = _gen_model_query_select(query if query is not None else self.__tableclass__,
                                    conds=conds,
                                    orders=orders,
                                    groups=groups,
                                    group_conds=group_conds,
                                    offset=offset,
                                    limit=limit)
        ans = session.execute(q)
        result = _get_result(ans, result_analysis=result)
        self._check_commit(session)
        return result

    def update(self, session: Session,
               sets: Dict[str, Any],
               conds: Optional[Union[List[_SQLCondOperations], _SQLCondOperations]] = None):
        """修改

        Args:
            session: 数据库session
            sets: 需要修改的字段值字典, 例如修改名称为xxx1, {'name': 'xxx1'}
            conds: 需要修改的属性的查询条件
        """
        up = update(self.__tableclass__).values(**sets)
        if conds:
            conds = _wrapper_to_list(conds)
            up = up.where(*conds)
        session.execute(up)
        self._check_commit(session)
        return True

    def delete(self, session: Session,
               conds: Optional[Union[List[_SQLCondOperations], _SQLCondOperations]] = None):
        """删除

        Args:
            session: 数据库session
            conds: 查询条件
        """
        if not conds:
            raise ValueError('删除数据查询条件不能为空')
        dt = delete(self.__tableclass__).where(*(_wrapper_to_list(conds)))
        session.execute(dt)
        self._check_commit(session)
        return True

    def _check_commit(self, session: Session):
        if self.__autocommit__:
            session.commit()


class AsyncBaseMapper:
    """提供表的基础操作封装"""

    # 表类型, 需要继承 DeclarativeBase
    __tableclass__: Type[_BASE] = None
    # 是否自动提交, 为True将会自动提交
    __autocommit__: bool = False

    def __init__(self):
        self._table = self.__tableclass__.__table__
        self._columns = []
        self._attr_column_map = {}
        self._primary_keys = []
        self._exclude_primary_columns = []
        for column in self._table.columns:
            self._columns.append(column.key)
            self._attr_column_map[column.key] = column.name
            if column.primary_key:
                self._primary_keys.append(column.key)
            else:
                self._exclude_primary_columns.append(column.key)

    async def save(self, session: AsyncSession, instance: _BASE, ignore_none: bool = True) -> bool:
        """新增或修改

        Args:
            session: 数据库session
            instance: 实例对象
            ignore_none: 忽略None值, 为True时新增和删除将会忽略none值
        """
        _type: Literal['add', 'update', None] = None
        # 按照所有主键查询是否存在
        conds = []
        for primary_key in self._primary_keys:
            conds.append(getattr(self.__tableclass__, primary_key) == getattr(instance, primary_key))
        # 查询, 存在则修改, 否则新增
        item = await self.query(session, conds=conds, limit=1, result='scalars-first')
        if not item:
            session.add(instance)
            await self._check_commit(session)
        else:
            if not conds:
                raise ValueError('表{}不存在主键, 无法通过该方法更新数据'.format(self.__tableclass__.__tablename__))
            sets = {}
            for attr_name in self._exclude_primary_columns:
                attr = getattr(instance, attr_name)
                if attr is not None or not ignore_none:
                    sets[self._attr_column_map[attr_name]] = attr
            if sets:
                await self.update(session, sets=sets, conds=conds)
        return True

    async def query_one(self, session: AsyncSession,
                        conds: Optional[Union[List[_SQLCondOperations], _SQLCondOperations]] = None,
                        orders: Optional[Union[List[_SQLOrderOperations], _SQLOrderOperations]] = None,
                        groups: Optional[Union[List[_SQLGroupOperations], _SQLGroupOperations]] = None,
                        group_conds: Optional[Union[List[_SQLHavingOperations], _SQLHavingOperations]] = None,
                        offset: Optional[int] = None,
                        limit: Optional[int] = None,
                        fields: Optional[_SQLSelectOperations] = None,
                        result: Literal[
                            'first', 'scalars-first', 'one_or_none', 'scalars-one_or_none', 'one', 'scalars-one', None] = 'scalars-first',
                        **kwargs) -> Union[ScalarResult[_BASE], Sequence[_BASE], _BASE, None, Any]:
        """条件查询, 仅返回单条记录, query的部分分支, 具体见query方法"""
        return await self.query(session, conds, orders, groups, group_conds, offset, limit, fields, result, **kwargs)

    async def query(self, session: AsyncSession,
                    conds: Optional[Union[List[_SQLCondOperations], _SQLCondOperations]] = None,
                    orders: Optional[Union[List[_SQLOrderOperations], _SQLOrderOperations]] = None,
                    groups: Optional[Union[List[_SQLGroupOperations], _SQLGroupOperations]] = None,
                    group_conds: Optional[Union[List[_SQLHavingOperations], _SQLHavingOperations]] = None,
                    offset: Optional[int] = None,
                    limit: Optional[int] = None,
                    query: Optional[_SQLSelectOperations] = None,
                    result: Literal[
                        'scalar', 'scalars', 'list', 'scalars-list', 'first', 'scalars-first', 'one_or_none', 'scalars-one_or_none', 'one', 'scalars-one', None] = 'scalars-list',
                    **kwargs) -> Union[ScalarResult[_BASE], Sequence[_BASE], _BASE, None, Any]:
        """条件查询

        Args:
            session: 数据库session
            conds: 条件, 例如 XXXTable.id == 2, XXXTable.id.in_(1, 2, 3), 传递该形式的条件
            orders: 排序, 例如 XXXTable.id.asc(), XXXTable.id.desc() 传递该形式参数
            groups: 分组
            group_conds: 分组条件
            offset: offset
            limit: limit
            query: 查询内容, 为 None 默认查询表所有字段, 允许传数据表属性字段及列表, 允许传递sqlalchemy.func函数及函数列表
            result: 返回数据形式, 默认 scalars_list, 各类型见源码

        Returns:
            ScalarResult或者List
        """
        q = _gen_model_query_select(query if query is not None else self.__tableclass__,
                                    conds=conds,
                                    orders=orders,
                                    groups=groups,
                                    group_conds=group_conds,
                                    offset=offset,
                                    limit=limit)
        ans = await session.execute(q)
        result = _get_result(ans, result_analysis=result)
        await self._check_commit(session)
        return result

    async def update(self, session: AsyncSession,
                     sets: Dict[str, Any],
                     conds: Optional[Union[List[_SQLCondOperations], _SQLCondOperations]] = None):
        """修改

        Args:
            session: 数据库session
            sets: 需要修改的字段值字典, 例如修改名称为xxx1, {'name': 'xxx1'}
            conds: 需要修改的属性的查询条件
        """
        up = update(self.__tableclass__).values(**sets)
        if conds:
            conds = _wrapper_to_list(conds)
            up = up.where(*conds)
        await session.execute(up)
        await self._check_commit(session)
        return True

    async def delete(self, session: AsyncSession,
               conds: Optional[Union[List[_SQLCondOperations], _SQLCondOperations]] = None):
        """删除

        Args:
            session: 数据库session
            conds: 查询条件
        """
        if not conds:
            raise ValueError('删除数据查询条件不能为空')
        dt = delete(self.__tableclass__).where(*(_wrapper_to_list(conds)))
        await session.execute(dt)
        await self._check_commit(session)
        return True

    async def _check_commit(self, session: AsyncSession):
        if self.__autocommit__:
            await session.commit()
