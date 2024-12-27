import abc
from typing import Union, Type, Callable, Any


class BeanFactory(abc.ABC):
    """Abstract class for Bean Factory"""

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_bean(self, name: str = None, required_type: Union[Type, Callable] = None):
        """Method to get a bean."""
        raise NotImplementedError

    def get_beans(self, required_type: Type):
        """Method to get a list of beans of a specific type."""
        raise NotImplementedError

    @abc.abstractmethod
    def register_bean(self, name: str, cls, primary: bool = False, order: int = 0, **kwargs) -> Any:
        """Method to register a bean."""
        raise NotImplementedError

    @abc.abstractmethod
    def init(self, **kwargs):
        """Initialization method for creating beans.
        Note:
             Note: This method may be executed repeatedly due to the Python module loading mechanism.
             In order to support pre dependency handling of IOC related operations executed during module loading.
        """
        raise NotImplementedError
