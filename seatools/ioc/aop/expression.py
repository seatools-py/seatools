import re
from typing import List, AnyStr, Optional


class PointExpression:

    def __init__(self, expression):
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
        expression = '^' + expression[0].strip().replace('*', '[a-zA-Z0-9]*').replace('..', '[a-zA-Z0-9.]*') + '$'
        return re.compile(expression)

    def match(self, path: str) -> bool:
        """Check expression against a path."""
        if not self._compile:
            return False
        return True if self._compile.match(path) else False
