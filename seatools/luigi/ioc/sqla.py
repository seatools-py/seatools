import abc
import os
import warnings

from luigi.contrib.sqla import SQLAlchemyTarget as SAT, CopyToTable as CTT
from seatools.ioc import Autowired


class SQLAlchemyTarget(SAT):
    """SQLAlchemyTarget setools.ioc implementation."""
    _engine_dict = {}

    def __init__(self, bean_name, target_table, update_id):
        super().__init__(connection_string='',
                         target_table=target_table,
                         update_id=update_id)
        self.bean_name = bean_name

    @property
    def engine(self):
        pid = os.getpid()
        conn = SQLAlchemyTarget._engine_dict.get(self.bean_name)
        if not conn or conn.pid != pid:
            # create and reset connection
            engine = Autowired(self.bean_name).engine()
            SQLAlchemyTarget._engine_dict[self.bean_name] = self.Connection(engine, pid)
        return SQLAlchemyTarget._engine_dict[self.bean_name].engine


class CopyToTable(CTT):
    """CopyToTable setools.ioc implementation."""

    @property
    def connection_string(self):
        warnings.warn('Departed. Use bean_name repeat it.', DeprecationWarning)
        return None

    @property
    @abc.abstractmethod
    def bean_name(self):
        return None

    def output(self):
        return SQLAlchemyTarget(
            bean_name=self.bean_name,
            target_table=self.table,
            update_id=self.update_id())
