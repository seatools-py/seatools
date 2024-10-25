from seatools.models import BaseModel
from clickhouse_driver import connect
from clickhouse_driver.dbapi.cursor import Cursor
from typing import Optional
from typing import Union, Any, List, Tuple, Type


class _DictCursor(Cursor):
    is_query = False

    def execute(self, operation, parameters=None):
        if str(operation).strip().lower().startswith('select'):
            self.is_query = True
        super().execute(operation, parameters=parameters)

    def executemany(self, operation, seq_of_parameters):
        if str(operation).strip().lower().startswith('select'):
            self.is_query = True
        super().executemany(operation, seq_of_parameters)

    def fetchall(self):
        rows = super().fetchall()
        if rows and self.is_query:
            columns = [column.name for column in self.description]
            rows = [dict(zip(columns, row)) for row in rows]
        return rows

    def fetchone(self):
        one = super().fetchone()
        if one and self.is_query:
            columns = [column.name for column in self.description]
            one = dict(zip(columns, one))
        return one

    def fetchmany(self, size=None):
        rows = super().fetchmany(size)
        if rows and self.is_query:
            columns = [column.name for column in self.description]
            rows = [dict(zip(columns, row)) for row in rows]
        return rows


class _ClickhouseConfig(BaseModel):
    host: Optional[str] = 'localhost'
    port: Optional[int] = 9000
    user: Optional[str] = None
    password: Optional[str] = None
    db: Optional[str] = None


class ClickhouseDriverClient:

    def __init__(self,
                 host='localhost',
                 port=9000,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 database: Optional[str] = None,
                 **kwargs):
        self._config = _ClickhouseConfig(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
        )
        self._kw = kwargs

    def execute(self,
                sql: str,
                args: Union[List[Any], Tuple[Any], None] = None,
                modelclass: Optional[Type[BaseModel]] = None) -> Union[
        List[dict], Tuple[dict], List[BaseModel], Tuple[BaseModel]]:
        conn = connect(
            host=self._config.host,
            port=self._config.port,
            user=self._config.user,
            password=self._config.password,
            database=self._config.db,
            **self._kw
        )
        cursor = conn.cursor(cursor_factory=_DictCursor)
        try:
            cursor.execute(sql, parameters=args)
            # 查询sql转为dict
            # if sql.strip().lower().startswith('select'):
            #     fields = [desc[0] for desc in ans.description]
            ans = cursor.fetchall()
            if ans and modelclass:
                ans = list(map(lambda e: modelclass(**e), ans))
            return ans
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
