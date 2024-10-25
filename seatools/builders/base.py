from abc import ABC, abstractmethod
from typing import Any


class BaseBuilder(ABC):
    """通用建造器父类, 所有建造器应继承该类"""

    @abstractmethod
    def build(self) -> Any:
        raise NotImplementedError()

    def __str__(self):
        return self.build()
