import abc
from typing import Any
from .point import JoinPoint


class AbstractAspect(abc.ABC):
    """Abstract aspect."""

    @property
    @abc.abstractmethod
    def pointcut(self) -> str:
        """Pointcut. Similar to `spring @Pointcut`

        example:
            class CustomAspect(AbstractAspect):

                pointcut = "execution(xxx.xxx..*xxx.*)" # only path and public method.

        note:
            Only support execution. Not support "annotation(...)", use decorator to repeat it.
        """
        pass

    def before(self, point: JoinPoint, **kwargs) -> None:
        """before aspect. Note: point.get_return_value() is None."""
        pass

    def around(self, point: JoinPoint, **kwargs) -> Any:
        """around aspect. Note: use point.process() to call aspect function."""
        return point.proceed()

    def after(self, point: JoinPoint, **kwargs) -> None:
        """after aspect."""
        pass

    def after_returning(self, point: JoinPoint, return_value: Any, **kwargs) -> None:
        """after success and returning aspect."""
        pass

    def after_exception(self, point: JoinPoint, ex: Exception, **kwargs) -> None:
        """after fail and raise exception aspect."""
        pass
