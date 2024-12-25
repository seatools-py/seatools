from typing import Any, Tuple, Dict


class JoinPoint:

    def __init__(self, path, instance, method_name, args: Tuple[Any, ...], kwargs: Dict[str, Any]):
        self.instance = instance
        self.method_name = method_name
        self.method = getattr(instance, method_name)
        self.args = args
        self.kwargs = kwargs
        self.return_value = None
        self.path = path

    def process(self) -> Any:
        """do point process."""
        self.return_value = self.method(*self.args, **self.kwargs)
        return self.return_value
