import inspect

from seatools.ioc.base import _register_bean


def bean(*args, name: str = None, primary=False):
    """bean装饰器

    Args:
        name: bean name
        primary: 是否默认, 当通过类型获取bean有多个bean时， 若无有primary或存在多个primary的bean将抛出异常, 仅当有一个primary时正常返回
    """

    def wrapper(fc=None):
        # 注册bean
        _register_bean(name=name, cls=fc, primary=primary)
        fc.__bean__ = True
        return fc

    if len(args) == 1 and (inspect.isclass(args[0]) or inspect.isfunction(args[0])):
        return wrapper(args[0])
    return wrapper


Bean = bean
