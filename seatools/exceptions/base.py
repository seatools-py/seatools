from typing import Union, Tuple, Type, TypeVar

_T = TypeVar('_T', bound=Exception)


def do_uncaught_exceptions(func, *args,
                           uncaught_exceptions: Union[
                               Type[_T], Tuple[Type[_T]]] = Exception,
                           **kwargs):
    """执行并忽略所有指定的异常

    Args:
        func: 执行的方法/函数
        uncaught_exceptions: 执行方法不处理的异常

    Returns:
        方法/函数执行成功返回对应的返回值, 失败返回None
    """
    try:
        return func(*args, **kwargs)
    except uncaught_exceptions:
        return None
