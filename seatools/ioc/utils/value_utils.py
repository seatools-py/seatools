from typing import Any, Type, Dict, List
from .type_utils import is_basic_type
from pydantic import BaseModel
import inspect


def convert(value: Any, _type: Type) -> Any:
    """将对象转为特定类型"""
    if value is None:
        return None
    if isinstance(value, _type):
        return value
    # 基本类型直接强转
    if is_basic_type(_type):
        return _type(value)
    if isinstance(value, dict):
        if issubclass(_type, BaseModel) or getattr(_type, '__dataclass_fields__', None) is not None:
            return _type(**value)
        return _new_model(value, _type)


def _new_model(data: Dict, model_class) -> Any:
    """针对非pydantic, 使用反射"""
    members = inspect.getmembers(model_class)
    class_args_annotations_map = {}
    init_args = []
    init_args_annotations_map = {}
    for member in members:
        if member[0] == '__annotations__':
            class_args_annotations_map = member[1]
        if member[0] == '__init__':
            init_spec = inspect.getfullargspec(member[1])
            init_args = init_spec.args[1:]  # 过滤self
            init_args_annotations_map = init_spec.annotations
    # 通过构造器创建对象
    obj = _new_model_by_init_args(data, model_class, init_args, init_args_annotations_map)
    init_args_set = set(init_args)
    for member_arg, _type in class_args_annotations_map.items():
        # 构造器初始化过的参数不处理
        if member_arg in init_args_set:
            continue
        v = data.get(member_arg)
        if v is not None:
            if _type:
                setattr(obj, member_arg, convert(v, _type))
                continue
            setattr(obj, member_arg, v)
            continue
    return obj


def _new_model_by_init_args(data: Dict, model_class, init_args: List, init_args_annotations_map: Dict):
    # 先处理构造器
    if not init_args:
        obj = model_class()
    else:
        init_params = {}
        for init_arg in init_args:
            v = data.get(init_arg)
            if v is not None:
                _type = init_args_annotations_map.get(init_arg)
                if _type:
                    init_params[init_arg] = convert(v, _type)
                    continue
                init_params[init_arg] = v
                continue
            init_params[init_arg] = None
        obj = model_class(**init_params)
    return obj
