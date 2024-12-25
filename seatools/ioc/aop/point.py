from typing import Any, Tuple, Dict


class JoinPoint:

    def __init__(self, path, target, method_name, args: Tuple[Any, ...], kwargs: Dict[str, Any]):
        """
        Args:
           path: pointcut module-class-method path. example: xxx.xxx.xxx.XxxClass.xxx_method
           target: pointcut proxy target
           method_name: pointcut method name
           args: pointcut method args
           kwargs: pointcut method kwargs
        """
        self.target = target
        self.method_name = method_name
        self.method = getattr(target, method_name)
        self.args = args
        self.kwargs = kwargs
        self.return_value = None
        self.path = path

    def proceed(self) -> Any:
        """do point method."""
        self.return_value = self.method(*self.args, **self.kwargs)
        return self.return_value

    def get_arg(self, index = None, field_name = None):
        """Get index arg or filed_name arg. Not contains self. Note: index and field_name cannot be empty at the same time.

        Args:
            index: get index base on args
            field_name: get field name base on kwargs
        """
        if len(self.args) > index:
            return
        assert index is not None or field_name, 'index and field_name cannot be empty at the same time.'
        arg = None
        if index is not None:
            arg = self.args[index]
        if field_name:
            arg = self.kwargs.get(field_name) or arg
        return arg
