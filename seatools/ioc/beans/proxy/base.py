import abc
from typing import Any


class BasicTypeMixin(abc.ABC):
    """基本数据类型Mixin."""
    @property
    def value(self):
        raise NotImplementedError()

    @property
    def int(self):
        return int(self.value)

    @property
    def float(self):
        return float(self.value)

    @property
    def bool(self):
        return bool(self.value)

    @property
    def str(self):
        return str(self.value)

    @property
    def list(self):
        return list(self.value)

    @property
    def dict(self):
        return dict(self.value)

    @property
    def tuple(self):
        return tuple(self.value)

    @property
    def set(self):
        return set(self.value)

    @property
    def complex(self):
        return complex(self.value)


class BaseBeanProxy(BasicTypeMixin, abc.ABC):
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
        return type(self.ioc_bean())

    def ioc_bean(self):
        """获取被代理的真实对象"""
        return self._obj

    def __getattr__(self, item):
        return getattr(self.ioc_bean(), item)

    def __getattribute__(self, item):
        if item.startswith('__') and item.endswith('__'):
            attr = getattr(self.ioc_bean(), item)
            if callable(attr):
                def wrapper(*args, **kwargs):
                    return attr(*args, **kwargs)

                return wrapper
            return attr
        return object.__getattribute__(self, item)

    def __setitem__(self, key, value):
        return self.ioc_bean().__setitem__(key, value)

    def __getitem__(self, item):
        return self.ioc_bean().__getitem__(item)

    def __delitem__(self, key):
        return self.ioc_bean().__delitem__(key)

    def __delattr__(self, item):
        return self.ioc_bean().__delattr__(item)

    def __eq__(self, other):
        return self.ioc_bean().__eq__(other)

    def __call__(self, *args, **kwargs):
        return self.ioc_bean()(*args, **kwargs)

    def __repr__(self):
        return self.ioc_bean().__repr__()

    @property
    def value(self):
        return self.ioc_bean()


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
        return isinstance(self.ioc_bean(), clazz)

    def primary(self):
        return self._primary
