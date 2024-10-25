import inspect


def is_family_type(class1, class2) -> bool:
    """检查两个类型是否同族, 支持函数, 类, 若为函数则必须相等

    Args:
        class1: 类型1
        class2: 类型2
    """
    if inspect.isfunction(class1) or inspect.isfunction(class2):
        return class1 == class2
    return issubclass(class1, class2) or issubclass(class2, class1)
