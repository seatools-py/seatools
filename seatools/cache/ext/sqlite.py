from cachetools import Cache as _Cache
from seatools.sqlalchemy import SqlAlchemyClient
from seatools.sqlalchemy import Base
from sqlalchemy import String
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import mapped_column


class _CacheData(Base):
    __tablename__ = 'cache'

    key = mapped_column(String, primary_key=True)
    value = mapped_column(String)


class SqliteCache(_Cache):
    """Sqlalchemy的sqlite缓存实现"""

    def __init__(self, maxsize, conn_url='sqlite:///cache.db', getsizeof=None):
        super().__init__(maxsize, getsizeof)
        self._conn_url = conn_url

    def _sqlite_cli(self) -> SqlAlchemyClient:
        if hasattr(self, '_sqlite_client') and self._sqlite_client:
            return self._sqlite_client
        self._sqlite_client = SqlAlchemyClient(self._conn_url)
        Base.metadata.create_all(self._sqlite_client.engine())
        return self._sqlite_client

    def __contains__(self, key):
        with self._sqlite_cli().session() as session:
            return session.query(_CacheData).where(_CacheData.key == key).count() > 0

    def __getitem__(self, key):
        with self._sqlite_cli().session() as session:
            cache_data = session.query(_CacheData).where(_CacheData.key == key).first()
            if cache_data:
                return cache_data.value
            raise KeyError(key)

    def __setitem__(self, key, value):
        with self._sqlite_cli().session() as session:
            session.execute(insert(_CacheData).values(key=key, value=value).on_conflict_do_update(
                index_elements=['key'],
                set_={'value': value}
            ))

    def __delitem__(self, key):
        with self._sqlite_cli().session() as session:
            session.query(_CacheData).where(_CacheData.key == key).delete()
