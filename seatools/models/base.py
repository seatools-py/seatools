from pydantic import BaseModel as BM, ConfigDict, Field
from pydantic.fields import FieldInfo
from abc import ABC
import datetime
from typing import Optional, Any, TypeVar, Generic, Sequence


class BaseModel(BM, ABC):
    """符合业务场景的通用基础Model"""

    model_config = ConfigDict(json_encoders={
        datetime.datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
    })

    def __init__(self, **kwargs):
        handlers = self._type_enhance_handlers()
        if handlers:
            for field_name, field_info in self.model_fields.items():
                for handler in handlers:
                    handler(field_name, field_info, kwargs)
        super().__init__(**kwargs)

    def _type_enhance_handlers(self):
        """类型增强处理

        handler 方法签名如下:

        def xxx_handler(field_name: str, field_info: pydantic.fields.FieldInfo, kwargs: dict) -> None:
            pass

        其中kwargs为输入参数字典

        子类可重写该方法拓展, 示例:
        class XXXModel(BaseModel):

             def _type_enhance_handlers(self):
                handlers = super()._type_enhance_handlers()
                # 添加自定义的增强逻辑
                handlers.append(...)
                return handlers
        """

        def enhance_str_type(field_name: str, field_info: FieldInfo, kwargs: dict):
            # 针对str类型, 额外支持int, float, bool类型转换
            if not field_info.annotation == str and not field_info.annotation == Optional[str]:
                return
            field_name = field_info.alias or field_name
            if not field_name in kwargs:
                return
            value = kwargs[field_name]
            if isinstance(value, (int, float)):
                kwargs[field_name] = str(value)
            elif isinstance(value, bool):
                kwargs[field_name] = str(value).lower()

        return [enhance_str_type]


_T = TypeVar('_T', bound=Any)


class R(BaseModel, Generic[_T]):
    """通用响应对象"""
    # 状态码
    code: int = Field(..., title='状态码')
    # 状态信息
    msg: str = Field(..., title='状态信息')
    # 响应数据
    data: Optional[_T] = Field(None, title='响应数据')

    @staticmethod
    def ok(data: Optional[Any] = None, msg: str = '请求成功', code: int = 200):
        return R(code=code, msg=msg, data=data)

    @staticmethod
    def fail(msg: str = '请求失败', code: int = 500):
        return R(code=code, msg=msg, data=None)


class PageModel(BaseModel, Generic[_T]):
    """分页Model, 可作分页入参可作分页出参, 入参仅需传入page, 与page_size, 出参则均需传入"""
    # 分页数据记录列表
    rows: Optional[Sequence[_T]] = Field([], title='分页数据记录列表')
    # 当前页码
    page: Optional[int] = Field(1, title='当前页码')
    # 当前页大写
    page_size: Optional[int] = Field(10, title='当前页大小')
    # 记录总数
    total: Optional[int] = Field(0, title='记录总数')


class PageR(R, Generic[_T]):
    """通用分页响应"""
    data: Optional[PageModel[_T]] = Field(..., title='响应数据')

    @staticmethod
    def ok(data: Optional[PageModel] = None, msg: str = '请求成功', code: int = 200):
        if not data:
            data = PageModel()
        return R.ok(code=code, msg=msg, data=data)
