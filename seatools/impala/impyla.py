from seatools.models import BaseModel
from impala.dbapi import connect
from typing import Optional, List, Tuple, Any, Union, Type


class _ImpylaConfig(BaseModel):
    host: Optional[str] = 'localhost'
    port: Optional[int] = 21050
    user: Optional[str] = None
    password: Optional[str] = None
    db: Optional[str] = None


class ImpylaClient:

    def __init__(self,
                 host='localhost',
                 port=21050,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 database: Optional[str] = None,
                 **kwargs):
        self._config = _ImpylaConfig(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
        )
        self._kw = kwargs

    def _new_connection(self):
        return connect(
            host=self._config.host,
            port=self._config.port,
            user=self._config.user,
            password=self._config.password,
            database=self._config.db,
            **self._kw
        )

    def execute(self,
                sql: str,
                args: Union[List[Any], Tuple[Any], None] = None,
                modelclass: Optional[Type[BaseModel]] = None) -> Union[
        List[dict], Tuple[dict], List[BaseModel], Tuple[BaseModel]]:
        conn = self._new_connection()
        cursor = conn.cursor(dictify=True)
        try:
            cursor.execute(sql, parameters=args)
            ans = cursor.fetchall()
            if ans and modelclass:
                ans = list(map(lambda e: modelclass(**e), ans))
            return ans
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
