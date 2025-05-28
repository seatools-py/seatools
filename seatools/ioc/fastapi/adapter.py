from seatools.ioc.injects import Autowired
from typing import TypeVar, Type, Any
from fastapi import Depends


_T = TypeVar("_T", bound=Any)


def from_bean(value: str = None, *, cls: Type[_T] = None, required: bool = True) -> _T:
    """
    适用于将seatools.ioc容器转换到FastAPI的依赖注入
    Args:
        value: seatools.ioc bean name
        cls:  seatools.ioc bean type
        required: 是否必须

    Returns:
        FastAPI 的 Depends 依赖注入对象, 注入的实际对象为 seatools.ioc 的容器实例
    """
    async def depends_bean() -> _T:
        return Autowired(value, cls=cls, required=required)

    return Depends(depends_bean)


FastAutowired = from_bean
