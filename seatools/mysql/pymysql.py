from seatools.models import BaseModel
from typing import Optional, Type, List, Tuple, Any, Union
from pymysql import connect as c, Connection
from pymysql.cursors import DictCursor
from contextlib import contextmanager


def connect(host=None,
            port=3306,
            user=None,
            password='',
            database=None,
            cursorclass=DictCursor,
            autocommit=True,
            pool=False,
            pool_size=1,
            **kwargs):
    """业务Pymysql连接通用参数封装

    Returns:
        pymysql.Connection or dbutils.pooled_db.PooledDB
    """
    if pool:
        from dbutils.pooled_db import PooledDB
        return PooledDB(creator=connect,
                        mincached=pool_size,
                        host=host,
                        port=port,
                        user=user,
                        password=password,
                        database=database,
                        cursorclass=cursorclass,
                        autocommit=autocommit,
                        **kwargs)
    return c(host=host,
             port=port,
             user=user,
             password=password,
             database=database,
             cursorclass=cursorclass,
             autocommit=autocommit,
             **kwargs)


class _PyMysqlConfig(BaseModel):
    host: str
    port: int
    user: str
    password: Optional[str] = ''
    db: Optional[str] = None
    autocommit: Optional[bool] = False


class _PyMysqlTransactionCursor:
    """pymysql 事务 cursor 拓展, 仅执行 SQL 不提交不回滚, 由 PyMysqlHelper 处理提交回滚连接"""

    def __init__(self, conn: Connection):
        self._conn = conn
        self._cursor = conn.cursor()

    def execute(self,
                sql: str,
                args: Union[List[Any], Tuple[Any], None] = None,
                modelclass: Optional[Type[BaseModel]] = None
                ):
        """以事务方式执行 sql, 保障同一个 对象 执行多次 execute 方法在同一事务中

        Args:
            sql: 执行的sql
            args: 执行的sql中的参数
            modelclass: pydantic model 类型, 传入该值会将结果转为 pydantic model
        """
        self._cursor.execute(sql, args)
        ans = self._cursor.fetchall()
        if ans and modelclass:
            ans = list(map(lambda e: modelclass(**e), ans))
        return ans

    def close(self):
        if self._cursor:
            self._cursor.close()


class PyMysqlClient:
    """pymysql 客户端"""

    def __init__(self,
                 host='localhost',
                 port=3306,
                 user='root',
                 password='',
                 database=None,
                 **kwargs):
        self._config = _PyMysqlConfig(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database
        )
        self._kw = kwargs

    def _new_connection(self):
        return c(host=self._config.host,
                 port=self._config.port,
                 user=self._config.user,
                 password=self._config.password,
                 db=self._config.db,
                 autocommit=self._config.autocommit,
                 **self._kw)

    def execute(self,
                sql: str,
                args: Union[List[Any], Tuple[Any], None] = None,
                modelclass: Optional[Type[BaseModel]] = None) -> Union[
        List[dict], List[BaseModel], Tuple[dict], Tuple[BaseModel]]:
        """执行 非事务模式 sql

        Args:
            sql: 执行的sql
            args: 执行的sql中的参数
            modelclass: pydantic model 类型, 传入该值会将结果转为 pydantic model
        """
        conn = self._new_connection()
        cursor = conn.cursor(cursor=DictCursor)
        try:
            cursor.execute(sql, args)
            conn.commit()
            ans = cursor.fetchall()
            if ans and modelclass:
                ans = list(map(lambda e: modelclass(**e), ans))
            return ans
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @contextmanager
    def transaction_client(self) -> _PyMysqlTransactionCursor:
        """获取事务游标对象

        使用方式
            helper = PyMysqlHelper(...)
            with helper.cursor() as cursor:
                users = cursor.execute('select * from user')
                cursor.execute('update user set user_name= "sss" where user_id=1')

        """
        conn = self._new_connection()
        transaction_cursor = _PyMysqlTransactionCursor(conn)
        try:
            yield transaction_cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            transaction_cursor.close()
            if conn:
                conn.close()
