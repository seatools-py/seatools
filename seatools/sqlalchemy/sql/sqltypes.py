from typing import Type, TypeVar

from sqlalchemy import JSON, Dialect
from pydantic import BaseModel
from sqlalchemy.sql.type_api import _TypeMemoDict

_T = TypeVar('_T', bound=BaseModel)


class ModelJson(JSON):
    """拓展sqlalchemy json类型支持pydantic BaseModel类型"""

    __visit_name__ = "JSON"

    def __init__(self, cls: Type[_T], none_as_null: bool = False):
        super().__init__(none_as_null)
        self._cls = cls

    def bind_processor(self, dialect):
        return lambda value: self._dialect_info_impl(dialect)['impl'].bind_processor(dialect)(value.model_dump(mode='json'))


    def result_processor(self, dialect, coltype):
        return lambda value: self._cls(**(self._dialect_info_impl(dialect)['impl'].result_processor(dialect, coltype)(value)))

    def python_type(self):
        return self._cls

    def _dialect_info_impl(self, dialect: Dialect):
        return super()._dialect_info(dialect)

    def _dialect_info(self, dialect: Dialect) -> _TypeMemoDict:
        return {"impl": self, "result": {}}
