from typing import Any
from .base import BaseBeanProxy
from seatools.ioc.constants import required


class DelayAutowiredClassBeanProxy(BaseBeanProxy):
    """延迟类bean代理"""

    def __init__(self, name: str, obj: Any, *args, **kwargs):
        """
        Args:
            obj: class 类型
        """
        super().__init__(name, None, *args, **kwargs)
        self._cls = obj

    def _delay_inject_obj(self):
        from seatools.ioc import get_application_context
        obj = get_application_context().get_bean(name=self._name, cls=self._cls)
        if self._extra_kwargs.get('required', True):
            if not obj:
                raise ValueError(
                    f'无法注入{("名称[" + self._name + "]") if self._name else ""}{("类型[" + self._cls.__name__ + "]") if self._cls.__name__ else ""}的bean')
        return obj

    def get(self):
        if self._obj is None:
            self._obj = self._delay_inject_obj()
        return self._obj

    def ioc_type(self):
        return self._cls


class DelayConfigAutowiredClassBeanProxy(BaseBeanProxy):

    def __init__(self, name: str, obj: Any, *args, **kwargs):
        """
        Args:
            name: 配置名称
            obj: 类型
        """
        super().__init__(name, None, *args, **kwargs)
        self._cls = obj

    def _delay_inject_obj(self):
        from seatools.ioc import get_environment
        env = get_environment()
        # 非ioc环境直接返回
        if not env:
            return None
        if not (self._name.startswith('${') and self._name.endswith('}')):
            raise ValueError('配置必须使用${}包裹')
        name = self._name[2:-1]
        v = env.get_property(name, cls=self._cls)
        if v is None:
            if self._extra_kwargs.get('default_value', required) == required:
                raise ValueError(f'{self._name}配置属性获取失败, 请检查配置')
            return self._extra_kwargs.get('default_value')
        return v

    def get(self):
        if self._obj is None:
            self._obj = self._delay_inject_obj()
        return self._obj

    def ioc_type(self):
        return self._cls
