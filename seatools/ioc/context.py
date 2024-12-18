from seatools.ioc.environment import Environment
from seatools.ioc.beans.factory import BeanFactory
from typing import Any


class ApplicationContext:

    def __init__(self, bean_factory: BeanFactory):
        self._bean_factory = bean_factory

    def get_bean(self, name=None, cls=None):
        """获取bean, bean不存在则返回None, name和cls不能同时为空

        Args:
            name: bean名称
            cls: 函数或类
        """
        if not name and not cls:
            raise ValueError('获取bean实例name与cls参数不能同时为空')
        if self._bean_factory:
            return self._bean_factory.get_bean(name=name, required_type=cls)
        return None

    def get_environment(self) -> Environment:
        return self._bean_factory.get_bean('environment', required_type=Environment)

    def get_bean_by_name(self, name: str):
        """通过名称获取bean

        Args:
            name: bean name

        Returns:
            bean obj or None
        """
        return self.get_bean(name=name)

    def get_bean_by_type(self, cls: Any):
        """通过类型获取bean

        Args:
            cls: bean type

        Returns:
            bean obj or None
        """
        return self.get_bean(cls=cls)
