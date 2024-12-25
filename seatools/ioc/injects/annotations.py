import inspect

from seatools.utils import list_utils
from seatools.ioc.base import _register_bean
from seatools.ioc.utils.name_utils import to_camel_case


def bean(*args, name: str = None, primary=False, order: int = 0):
    """bean装饰器

    Args:
        name: bean name
        primary: 是否默认, 当通过类型获取bean有多个bean时， 若无有primary或存在多个primary的bean将抛出异常, 仅当有一个primary时正常返回
        order: bean加载顺序, 值越小越先加载, 若依赖bean order值大于当前bean, 则会优先等待依赖加载后再做加载
    """

    def wrapper(fc=None):
        # 注册bean
        _register_bean(name=name, cls=fc, primary=primary, order=order)
        fc.__bean__ = True
        return fc

    if len(args) == 1 and (inspect.isclass(args[0]) or inspect.isfunction(args[0])):
        return wrapper(args[0])

    name = list_utils.get(args, 0, name)
    primary = list_utils.get(args, 1, primary)
    return wrapper


Bean = bean


def configuration_properties_bean(*args, prop: str = None, name: str = None, primary=False, order: int = 0):
    """配置属性bean. 仅支持pydantic model, dataclass, 同配置的构造函数, 仅支持非必填构造器, 若需要注入的构造参数默认值请使用unique_tools.ioc.Autowired()代替.

    Args:
        prop: 属性描述
        name: bean name
        primary: 是否默认, 当通过类型获取bean有多个bean时， 若无有primary或存在多个primary的bean将抛出异常, 仅当有一个primary时正常返回
        order: bean加载顺序, 值越小越先加载, 若依赖bean order值大于当前bean, 则会优先等待依赖加载后再做加载
    """

    def wrapper(fc=None):
        # 注册bean
        if inspect.isfunction(fc):
            fc = type(fc())
        elif not inspect.isclass(fc):
            fc = type(fc)

        def lazy_register_bean():
            from seatools.ioc import get_environment
            from seatools.ioc.environment import Environment
            e: Environment = get_environment()
            return e.get_property(prop, fc)

        _register_bean(name=name or to_camel_case(fc.__name__, False), cls=lazy_register_bean, primary=primary)
        fc.__bean__ = True
        return fc

    if len(args) == 1 and (inspect.isclass(args[0]) or inspect.isfunction(args[0])):
        return wrapper(args[0])

    prop = list_utils.get(args, 0, prop)
    name = list_utils.get(args, 1, name)
    primary = list_utils.get(args, 2, primary)
    return wrapper


ConfigurationPropertiesBean = configuration_properties_bean


def aspect_bean(*args, name: str = None, primary=False, order: int = 0):
    """bean装饰器

    Args:
        name: bean name
        primary: 是否默认, 当通过类型获取bean有多个bean时， 若无有primary或存在多个primary的bean将抛出异常, 仅当有一个primary时正常返回
        order: bean加载顺序或者aop执行顺序, 该值越大aop越先执行(与ioc bean加载相反)
    """

    def wrapper(fc=None):
        # 注册bean
        _register_bean(name=name, cls=fc, primary=primary, order=order, aspect=True)
        fc.__bean__ = True
        return fc

    if len(args) == 1 and (inspect.isclass(args[0]) or inspect.isfunction(args[0])):
        return wrapper(args[0])

    name = list_utils.get(args, 0, name)
    primary = list_utils.get(args, 1, primary)
    return wrapper


Aspect = AspectBean = aspect_bean
