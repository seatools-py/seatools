from typing import Any, Type, TypeVar, Union

from seatools.ioc.beans.proxy import DelayAutowiredClassBeanProxy, DelayConfigAutowiredClassBeanProxy
from seatools.ioc.beans.proxy.base import BasicTypeMixin
from seatools.ioc.constants import required as default_required

_T = TypeVar('_T', bound=Any)


class Autowired:
    """依赖自动注入"""

    def __new__(_, value: str = None, *, cls: Type[_T]=None, required: bool = True) -> _T:
        """注入对象

        Args:
            value: bean name
            cls: 类型
            required: 是否必须, 为true找不到注入对象会报错
        """
        return DelayAutowiredClassBeanProxy(name=value, obj=cls, required=required)


class Value:
    """配置自动注入"""
    _cache = {}

    def __new__(_, value: str, *args, cls: Type[_T]=None, default_value=default_required) -> Union[_T, BasicTypeMixin]:
        """参数注入

        Args:
            value: 配置名称, 多级使用.分隔, 示例: xxx.xxx
            cls: value读取数据的类型, 如果为None则返回环境变量中的值
            default_value: 默认值, 若不传则表示必须有配置值
        """
        if not value:
            raise ValueError('value配置名称不能为空')
        return DelayConfigAutowiredClassBeanProxy(name=value, obj=cls, default_value=default_value)
