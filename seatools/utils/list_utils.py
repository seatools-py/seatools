from typing import List, Tuple, Union, Any


def get(l: Union[List[Any], Tuple[Any, ...]], index: int, _default=None) -> Any:
    return l[index] if len(l) > index else _default

