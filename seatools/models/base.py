from pydantic import BaseModel as BM, ConfigDict, Field
from abc import ABC
import datetime
from typing import Optional, Any, List


class BaseModel(BM, ABC):
    """符合业务场景的通用基础Model"""

    model_config = ConfigDict(json_encoders={
        datetime.datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
    })

    def __init__(self, **kwargs):
        # 针对str类型, 额外支持int, float, bool类型转换
        for field_name, field_type in self.__annotations__.items():
            if field_type == str or field_type == Optional[str]:
                if field_name in kwargs:
                    value = kwargs[field_name]
                    if isinstance(value, (int, float)):
                        kwargs[field_name] = str(value)
                    elif isinstance(value, bool):
                        kwargs[field_name] = str(value).lower()
        super().__init__(**kwargs)


class R(BaseModel):
    """通用响应对象"""
    # 状态码
    code: int = Field(..., title='状态码')
    # 状态信息
    msg: str = Field(..., title='状态信息')
    # 响应数据
    data: Optional[Any] = Field(None, title='响应数据')

    @staticmethod
    def ok(data: Optional[Any] = None, msg: str = '请求成功', code: int = 200):
        return R(code=code, msg=msg, data=data)

    @staticmethod
    def fail(msg: str = '请求失败', code: int = 500):
        return R(code=code, msg=msg, data=None)


class PageModel(BaseModel):
    """分页Model, 可作分页入参可作分页出参, 入参仅需传入page, 与page_size, 出参则均需传入"""
    # 分页数据记录列表
    rows: Optional[List[Any]] = Field([], title='分页数据记录列表')
    # 当前页码
    page: Optional[int] = Field(..., title='当前页码')
    # 当前页大写
    page_size: Optional[int] = Field(..., title='当前页大小')
    # 记录总数
    total: Optional[int] = Field(..., title='记录总数')


class PageR(R):
    """通用分页响应"""
    data: Optional[PageModel] = Field(..., title='响应数据')

    @staticmethod
    def ok(data: Optional[PageModel] = None, msg: str = '请求成功', code: int = 200):
        if not data:
            data = PageModel()
        return R.ok(code=code, msg=msg, data=data)
