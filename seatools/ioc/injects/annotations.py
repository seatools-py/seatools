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


def configuration_properties_bean(*args, prop: str = None, name: str = None, primary=False):
    """配置属性bean. 仅支持pydantic model, dataclass, 同配置的构造函数, 仅支持非必填构造器, 若需要注入的构造参数默认值请使用unique_tools.ioc.Autowired()代替.

    Args:
        prop: 属性描述
        name: bean name
        primary: 是否默认, 当通过类型获取bean有多个bean时， 若无有primary或存在多个primary的bean将抛出异常, 仅当有一个primary时正常返回
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

        _register_bean(name=name, cls=lazy_register_bean, primary=primary)
        fc.__bean__ = True
        return fc

    if len(args) == 1 and (inspect.isclass(args[0]) or inspect.isfunction(args[0])):
        return wrapper(args[0])
    return wrapper


ConfigurationPropertiesBean = configuration_properties_bean
