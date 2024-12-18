import abc
from typing import Union, Type, Callable, Any


class BeanFactory(abc.ABC):
    """Bean工厂抽象类"""

    @abc.abstractmethod
    def get_bean(self, name: str = None, required_type: Union[Type, Callable] = None):
        """获取bean方法."""
        raise NotImplementedError

    def get_beans(self, required_type: Type):
        """获取某个类型的bean列表方法."""
        raise NotImplementedError

    @abc.abstractmethod
    def register_bean(self, name: str, cls, primary: bool = False, **kwargs) -> Any:
        """bean注册方法."""
        raise NotImplementedError

    @abc.abstractmethod
    def init(self, **kwargs):
        """创建bean的初始化方法."""
        raise NotImplementedError
