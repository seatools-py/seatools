import re


def to_camel_case(name: str, upper_case: bool = False) -> str:
    """转为驼峰

    Args:
        name: 转换的名称
        upper_case: True=大驼峰, False=小驼峰
    """
    if not name:
        return name
    if len(name) == 1:
        return name.upper() if upper_case else name.lower()
    items = re.split(r'[_\s]+', name)
    if len(items) == 1:
        return _to_camel_case_item(items[0], upper_case=upper_case)
    return _to_camel_case_item(items[0], upper_case=upper_case) + ''.join(_to_camel_case_item(x, upper_case=True) for x
                                                                          in items[1:])


def _to_camel_case_item(name: str, upper_case: bool = False) -> str:
    if not name:
        return name
    if len(name) == 1:
        return name.upper() if upper_case else name.lower()
    return name.title() if upper_case else (name[0].lower() + name[1:])
