import inspect
import queue
import importlib
from typing import Any, Type, Callable, Union, Optional, List, Dict

from ..proxy import *
from ...utils import name_utils
from .base import BeanFactory
from .initializing_bean import InitializingBean
from ...injects.objects import Autowired
from ...utils.type_utils import is_basic_type


class _Param:
    name: str
    cls: Any
    primary: bool

    def __init__(self, name: str = None, cls: Any = None, primary: bool = False):
        self.name = name
        self.cls = cls
        self.primary = primary


class SimpleBeanFactory(BeanFactory):
    """简单bean工厂"""

    def __init__(self):
        self._name_bean = {}
        self._type_bean = {}
        self._init_queue = queue.Queue()
        self._dependency_map = {}
        self._register_class_object_bean(name='simpleBeanFactory', obj=self)
        self._initialized = False

    def get_bean(self, name: str = None, required_type: Union[Type, Callable] = None) -> Any:
        if not name and not required_type:
            raise ValueError('bean名称和类型不能都为空')
        if name:
            return self._resolve_name_bean(name, required_type)
        return self._resolve_type_bean(required_type)

    def _resolve_bean_from_beans(self, beans):
        if len(beans) >= 2:
            for bean in beans:
                # 有primary返回primary
                if bean.primary():
                    return bean
            if len(beans) >= 2:
                raise RuntimeError('获取的bean数量不能超过1个, 请增加名称/类型获取bean或给某个bean配置primary属性')
        if beans:
            return beans[0]
        return None

    def _resolve_name_bean(self, name: str, required_type: Union[Type, Callable] = None):
        beans = self._name_bean.get(name)
        if not beans:
            return None
        # 特定类型
        if required_type:
            # 优先取相同类型的
            bean = self._resolve_bean_from_beans([bean for bean in beans if bean.ioc_type() == required_type])
            if bean:
                return bean
            # 同类型的未找到再找父类
            bean = self._resolve_bean_from_beans(
                [bean for bean in beans if issubclass(bean.ioc_type(), required_type)])
            if bean:
                return bean
            return None

        return self._resolve_bean_from_beans(beans)

    def _resolve_type_bean(self, required_type=None):
        beans = self._type_bean.get(required_type)
        if not beans:
            beans = []
            for _type in self._type_bean.keys():
                if issubclass(_type, required_type):
                    beans = [*beans, *self._type_bean[_type]]
        return self._resolve_bean_from_beans(beans)

    def _register_function_bean(self, name: str, func, primary: bool = False) -> Any:
        name = name or name_utils.to_camel_case(func.__name__, upper_case=False)
        proxy = ClassBeanProxy(name=name, obj=self._new_function_bean(func), primary=primary)
        self._add_bean(proxy.ioc_name(), proxy.ioc_type(), proxy)
        return proxy

    def _register_class_object_bean(self, name, obj, primary: bool = False) -> Any:
        name = name or name_utils.to_camel_case(obj.__class__.__name__, upper_case=False)
        proxy = ClassBeanProxy(name=name, obj=obj, primary=primary)
        self._add_bean(proxy.ioc_name(), proxy.ioc_type(), proxy)
        return proxy

    def _register_class_bean(self, name: str, cls, primary: bool = False) -> Any:
        return self._register_class_object_bean(name, self._new_class_bean(cls), primary=primary)


    def _new_class_bean(self, cls) -> Any:
        params = self._extract_func_enable_autowired_args(cls)
        return cls(**params)

    def _new_function_bean(self, func) -> Any:
        params = self._extract_func_enable_autowired_args(func)
        return func(**params)

    def _extract_fun_depends_args(self, func) -> dict:
        """抽取函数依赖参数信息."""
        signature = inspect.signature(func)
        params = {}
        for name, parameter in signature.parameters.items():
            annotation = parameter.annotation
            default = parameter.default
            # 默认值不为空 则 不注入参数
            if default is not parameter.empty:
                continue
            # 没有类型 或 是基本类型 则 不注入参数
            if annotation is parameter.empty or is_basic_type(annotation):
                continue
            # 参数名称和类型映射
            # 非字符串类型则直接返回类型
            if not isinstance(annotation, str):
                params[name] = annotation
            else:
                # 动态加载类型
                params[name] = getattr(importlib.import_module(inspect.getmodule(func).__name__), annotation)

        return params

    def _extract_class_attr_depends_args(self, cls) -> dict:
        """抽取类属性依赖参数信息."""
        members = [member for member in inspect.getmembers(cls) if issubclass(type(member[-1]), BaseBeanProxy)]
        return {member[0]: member[-1].ioc_type() for member in members}

    def _extract_func_enable_autowired_args(self, func) -> dict:
        """抽取函数可注入参数."""
        params = self._extract_fun_depends_args(func)
        if params:
            for name, cls in params.items():
                params[name] = Autowired(cls=cls)
        return params

    def register_bean(self, name: str, cls, primary: bool = False, lazy=True) -> Any:
        # 注册bean懒加载, 在init方法执行bean创建逻辑
        if lazy and not self._initialized:
            self._init_queue.put(_Param(name, cls, primary))
        else:
            self._register_bean(name, cls, primary)

    def _register_bean(self, name: str, cls, primary: bool = False) -> Any:
        if inspect.isfunction(cls):
            return self._register_function_bean(name, cls, primary=primary)
        if inspect.isclass(cls):
            return self._register_class_bean(name, cls, primary=primary)
        # 否则直接视为对象注册
        return self._register_class_object_bean(name, cls, primary=primary)

    def init(self):
        """初始化容器, 在bean都注册进工厂队列后执行, 同时解决多个容器间的依赖问题"""
        # 创建容器
        self._create_beans()
        # 初始化
        self._do_beans_init()
        self._initialized = True

    def _do_beans_init(self):
        # 对所有容器执行__post_construct__, InitializingBean.after_properties_set 初始化方法
        for beans in self._name_bean.values():
            for bean in beans:
                # 容器原始类型是类才能执行
                if inspect.isclass(bean.ioc_type()):
                    if hasattr(bean.ioc_type(), '__post_construct__'):
                        bean.__post_construct__()
                    if issubclass(bean.ioc_type(), InitializingBean):
                        bean.after_properties_set()

    def _create_beans(self):
        depends = []
        # 优先创建无依赖的bean
        while True:
            try:
                param: _Param = self._init_queue.get(block=False)
                # 没有依赖则可以直接注册bean
                depends_params = self._get_depends_args(param)
                if not depends_params:
                    self._register_bean(param.name, param.cls, param.primary)
                    continue
                # 依赖入队列
                depends.append({'param': param, 'depends': depends_params})
            except queue.Empty:
                break

        if not depends:
            return
        # 创建依赖bean
        self._create_depends_beans(depends)

    def _create_depends_beans(self, depends: List[Dict[str, Any]]):
        # 处理非循环依赖
        while True:
            end = True
            next_depends = []
            for dep in depends:
                params = {}
                for name, cls in dep['depends'].items():
                    # 获取依赖bean实例
                    obj = self.get_bean(name=name, required_type=cls) or self.get_bean(required_type=cls)
                    # 依赖bean不存在则跳过处理下一个
                    if obj is None:
                        break
                    params[name] = obj
                # 获取的依赖数量与目标一致则可以创建bean
                if len(params) == len(dep['depends']):
                    self._register_bean(dep['param'].name, dep['param'].cls, dep['param'].primary)
                    end = False
                else:
                    next_depends.append(dep)
            depends = next_depends
            # 没有需要解决的普通依赖就退出
            if end:
                break

        if not depends:
            return

        # 处理循环依赖
        for dep in depends:
            self._register_bean(dep['param'].name, dep['param'].cls, dep['param'].primary)

    def _get_depends_args(self, param: _Param) -> Optional[dict]:
        """判断要创建的bean是否存在依赖
        """
        name, cls, primary = param.name, param.cls, param.primary
        if inspect.isfunction(cls):
            # 属性Autowired依赖
            args = self._extract_class_attr_depends_args(cls)
            # 构造函数依赖
            args.update(self._extract_fun_depends_args(cls))
            return args
        if inspect.isclass(cls):
            return self._extract_fun_depends_args(cls)
        # 对象注入无需依赖
        return None

    def _add_bean(self, name: str, _type, bean: Any):
        self._add_name_bean(name, bean)
        self._add_type_bean(_type, bean)

    def _add_name_bean(self, name: str, bean: Any):
        beans = self._name_bean.get(name) or []
        beans.append(bean)
        self._name_bean[name] = beans

    def _add_type_bean(self, _type, bean: Any):
        beans = self._type_bean.get(_type) or []
        beans.append(bean)
        self._type_bean[_type] = beans
