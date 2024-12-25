import abc
import re
from typing import List, AnyStr, Optional


class AbstractMatcher(abc.ABC):

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def match(self, path: str) -> bool:
        pass


class AspectPointExpressionMather(AbstractMatcher):

    def __init__(self, expression, **kwargs):
        super().__init__(**kwargs)
        self.expression = expression
        self._patterns: List[re.Pattern[AnyStr]] = [re.compile('execution\s*\((.*)\)\s*')]
        self._compile = self.compile(expression)

    def compile(self, expression: str) -> Optional[re.Pattern[AnyStr]]:
        """compile a point expression."""
        assert expression, 'expression cannot be empty.'
        if not expression:
            return None
        expression = expression.strip()
        expression = self._patterns[0].findall(expression)
        if not expression:
            return None
        expression = '^' + expression[0].strip().replace('*', '([a-zA-Z0-9][a-zA-Z0-9_]*)').replace('..', '[a-zA-Z0-9._]*') + '$'
        return re.compile(expression)

    def match(self, path: str) -> bool:
        """Check expression against a path."""
        if not self._compile:
            return False
        return True if self._compile.match(path) else False
