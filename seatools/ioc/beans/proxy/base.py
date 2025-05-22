import abc
import warnings
import inspect
from typing import Any

from seatools.ioc.aop.point import JoinPoint


class BasicTypeMixin(abc.ABC):
    """基本数据类型Mixin."""

    @property
    def value(self):
        raise NotImplementedError

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
        self.ioc_initialized = False
        self._extra_args = args
        self._extra_kwargs = kwargs

    def ioc_name(self) -> str:
        """获取bean名称"""
        return self._name

    def ioc_type(self):
        """获取被代理的类型"""
        return type(self.value)

    def ioc_bean(self):
        """获取被代理的对象."""
        return self._obj

    def __getattr__(self, item):
        return getattr(self.ioc_bean(), item)

    def __getattribute__(self, item):
        if item.startswith('__') and item.endswith('__'):
            attr = getattr(self.ioc_bean(), item)
            if item in ('__getattribute__', '__getattr__', '__setattr__', '__delattr__'):
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
        v = self.ioc_bean()
        while issubclass(type(v), BaseBeanProxy):
            v = v.ioc_bean()
        return v


class ClassBeanProxy(BaseBeanProxy):
    """类对象bean代理"""

    def __init__(self, name: str, obj: Any, primary: bool = False, order: int = 0, *args, **kwargs):
        """
        Args:
            obj: 特定类的对象
        """
        super().__init__(name, obj, *args, **kwargs)
        self._primary = primary
        self._order = order

    def instanceof(self, clazz):
        """判断实际对象是否是某个类型的实例"""
        return isinstance(self.ioc_bean(), clazz)

    def primary(self):
        warnings.warn("Deprecated. Use ioc_primary to repeat it.", DeprecationWarning)
        return self._primary

    def ioc_primary(self):
        return self._primary

    def ioc_order(self):
        return self._order


class AsyncCallClassBeanProxy(ClassBeanProxy):

    async def __call__(self, *args, **kwargs):
        return await self.ioc_bean()(*args, **kwargs)


def get_real_type(obj):
    if issubclass(type(obj), BaseBeanProxy):
        return obj.ioc_type()
    return type(obj)


class AspectClassBeanProxy(BaseBeanProxy):

    def __init__(self, name: str, obj: Any, aspect, *args, **kwargs):
        """
        Args:
            obj: 特定类的对象
        """
        super().__init__(name, obj, *args, **kwargs)
        self._aspect = aspect

    def __getattr__(self, item):
        attr = getattr(self.ioc_bean(), item)
        if not callable(attr) or not self._aspect:
            return attr

        def wrapper(*args, **kwargs):
            target = self.ioc_bean()
            join_point = JoinPoint(
                path=inspect.getmodule(target).__name__ + '.' + get_real_type(target).__name__ + '.' + item,
                target=target,
                method_name=item,
                args=args,
                kwargs=kwargs)
            self._aspect.before(join_point)
            try:
                value = self._aspect.around(join_point)
                self._aspect.after_returning(join_point, value)
                return value
            except Exception as ex:
                self._aspect.after_exception(join_point, ex)
                raise ex
            finally:
                self._aspect.after(join_point)

        return wrapper
