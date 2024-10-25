import abc
from typing import Any


class BaseBeanProxy(abc.ABC):
    """基础代理, 未提供代理逻辑实现, 仅提供抽象封装"""
    _exclude_attr = []

    def __init__(self, name: str, obj: Any, *args, **kwargs):
        """

        Args:
             name: 代理bean名称
             obj: 需要被代理的对象
        """
        self._name = name
        self._obj = obj
        self._extra_args = args
        self._extra_kwargs = kwargs

    def ioc_name(self) -> str:
        """获取bean名称"""
        return self._name

    def ioc_type(self):
        """获取被代理的类型"""
        return type(self.get())

    def get(self):
        """获取被代理的真实对象"""
        return self._obj

    def __getattr__(self, item):
        return getattr(self.get(), item)

    def __getattribute__(self, item):
        if item.startswith('__') and item.endswith('__'):
            attr = getattr(self.get(), item)
            if callable(attr):
                def wrapper(*args, **kwargs):
                    return attr(*args, **kwargs)

                return wrapper
            return attr
        return object.__getattribute__(self, item)

    def __call__(self, *args, **kwargs):
        return self.get()(*args, **kwargs)

    def __repr__(self):
        return self.get().__repr__()


class ClassBeanProxy(BaseBeanProxy):
    """类对象bean代理"""

    def __init__(self, name: str, obj: Any, *args, primary: bool = False, **kwargs):
        """
        Args:
            obj: 特定类的对象
        """
        super().__init__(name, obj, *args, **kwargs)
        self._primary = primary

    def instanceof(self, clazz):
        """判断实际对象是否是某个类型的实例"""
        return isinstance(self.get(), clazz)

    def primary(self):
        return self._primary
