from typing import Any

from seatools.ioc.aop.aspect import AbstractAspect
from seatools.ioc.aop.matcher import AspectPointExpressionMather
from seatools.ioc.aop.point import JoinPoint


class SelectorAspect(AbstractAspect):

    def __init__(self, aspect: AbstractAspect):
        self.aspect = aspect
        self.mather = AspectPointExpressionMather(self.aspect.pointcut)
        self._cache = {}

    @property
    def pointcut(self) -> str:
        return self.aspect.pointcut

    def _match(self, point: JoinPoint):
        match = self._cache.get(point.path)
        if match is not None:
            return match
        match = self.mather.match(point.path)
        self._cache[point.path] = match
        return match

    def before(self, point: JoinPoint, **kwargs) -> None:
        if self._match(point):
            return self.aspect.before(point, **kwargs)
        return super().before(point, **kwargs)

    def around(self, point: JoinPoint, **kwargs) -> Any:
        if self._match(point):
            return self.aspect.around(point)
        return super().around(point, **kwargs)

    def after(self, point: JoinPoint, **kwargs) -> None:
        if self._match(point):
            return self.aspect.after(point, **kwargs)
        return super().after(point, **kwargs)

    def after_returning(self, point: JoinPoint, return_value: Any, **kwargs) -> None:
        if self._match(point):
            return self.aspect.after_returning(point, return_value, **kwargs)
        return super().after_returning(point, return_value, **kwargs)

    def after_exception(self, point: JoinPoint, ex: Exception, **kwargs) -> None:
        if self._match(point):
            return self.aspect.after_exception(point, ex, **kwargs)
        return super().after_exception(point, ex, **kwargs)
