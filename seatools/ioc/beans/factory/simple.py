import inspect
import queue
import importlib
from typing import Any, Type, Callable, Union, Optional, List, Dict, TypeVar, Tuple

from ..proxy import *
from ...aop.selector import SelectorAspect
from ...utils import name_utils
from .base import BeanFactory
from .initializing_bean import InitializingBean
from ...injects.objects import Autowired
from ...utils.type_utils import is_basic_type

_T = TypeVar('_T', bound=Any)


class _Param:
    name: str
    cls: Any
    primary: bool
    aspect: bool
    order: int

    def __init__(self, name: str = None, cls: Any = None, primary: bool = False, aspect: bool = False, order: int = 0):
        self.name = name
        self.cls = cls
        self.primary = primary
        self.aspect = aspect
        self.order = order

    def __lt__(self, other):
        return False


class SimpleBeanFactory(BeanFactory):
    """简单bean工厂"""

    def __init__(self, enable_aspect: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._initialized = False
        self._enable_aspect = enable_aspect
        self._name_bean = {}
        self._type_bean = {}
        self._aspect_bean = []
        self._init_queue = queue.PriorityQueue()
        self._register_class_object_bean(name='simpleBeanFactory', obj=self)

    def get_bean(self, name: str = None, required_type: Union[Type, Callable] = None) -> Any:
        if not name and not required_type:
            raise ValueError('bean名称和类型不能都为空')
        if name:
            return self._resolve_name_bean(name, required_type)
        return self._resolve_type_bean(required_type)

    def get_beans(self, required_type: Type[_T]) -> List[_T]:
        return [*(self._resolve_type_beans(required_type))]

    def _resolve_bean_from_beans(self, beans):
        if len(beans) >= 2:
            for bean in beans:
                # 有primary返回primary
                if bean.ioc_primary():
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
        beans = self._resolve_type_beans(required_type=required_type)
        return self._resolve_bean_from_beans(beans)

    def _resolve_type_beans(self, required_type=None):
        beans = self._type_bean.get(required_type)
        if not beans:
            beans = []
            for _type in self._type_bean.keys():
                if issubclass(_type, required_type):
                    beans = [*beans, *self._type_bean[_type]]
        return beans

    def _register_function_bean(self, name: str, func, primary: bool = False, aspect: bool = False,
                                order: int = 0) -> Any:
        name = name or name_utils.to_camel_case(func.__name__, upper_case=False)
        return self._register_class_object_bean(name, self._new_function_bean(func), primary=primary, aspect=aspect,
                                                order=order)

    def _register_class_object_bean(self, name, obj, primary: bool = False, aspect: bool = False,
                                    order: int = 0) -> Any:
        name = name or name_utils.to_camel_case(obj.__class__.__name__, upper_case=False)
        proxy = ClassBeanProxy(name=name, obj=obj, primary=primary, order=order, aspect=aspect)
        if self._enable_aspect:
            if aspect:
                self._aspect_bean.append(proxy)
                self._rebuild_bean_from_aspect(proxy)
            else:
                proxy = self._build_bean_by_aspects(proxy)
        self._add_bean(proxy.ioc_name(), proxy.ioc_type(), proxy)
        return proxy

    def _register_class_bean(self, name: str, cls, primary: bool = False, aspect: bool = False, order: int = 0) -> Any:
        return self._register_class_object_bean(name, self._new_class_bean(cls), primary=primary, aspect=aspect,
                                                order=order)

    def _new_class_bean(self, cls) -> Any:
        params = self._extract_func_enable_autowired_args(cls)
        return cls(**params)

    def _new_function_bean(self, func) -> Any:
        params = self._extract_func_enable_autowired_args(func)
        return func(**params)

    def _extract_fun_depends_args(self, func) -> Tuple[dict, dict]:
        """抽取函数依赖参数信息."""
        signature = inspect.signature(func)
        params, name_params = {}, {}
        for name, parameter in signature.parameters.items():
            annotation = parameter.annotation
            default = parameter.default
            # Autowired参数依赖顺序处理
            is_bean_proxy_type = issubclass(type(default), BaseBeanProxy)
            # 默认值不为空 则 不注入参数
            if default is not parameter.empty and not is_bean_proxy_type:
                continue
            # 代理类型默认值且annotation为空则通过代理对象获取被代理类型
            if is_bean_proxy_type:
                if annotation is parameter.empty:
                    annotation = default.ioc_type()
                name_params[name] = default.ioc_name()
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

        return params, name_params

    def _extract_class_attr_depends_args(self, cls) -> Tuple[dict, dict]:
        """抽取类属性依赖参数信息."""
        members = [member for member in inspect.getmembers(cls) if issubclass(type(member[-1]), BaseBeanProxy)]
        return {member[0]: member[-1].ioc_type() for member in members}, {member[0]: member[-1].ioc_name() for member in members}

    def _extract_func_enable_autowired_args(self, func) -> dict:
        """抽取函数可注入参数."""
        params, name_params = self._extract_fun_depends_args(func)
        if params:
            for name, cls in params.items():
                params[name] = Autowired(value=name_params.get(name), cls=cls)
        return params

    def register_bean(self, name: str, cls, primary: bool = False, order: int = 0, lazy=True,
                      aspect: bool = False) -> Any:
        # 注册bean懒加载, 在init方法执行bean创建逻辑
        if lazy and not self._initialized:
            self._init_queue.put((order, _Param(name, cls, primary, aspect, order)))
        else:
            self._register_bean(name, cls, primary, aspect, order)

    def _register_bean(self, name: str, cls, primary: bool = False, aspect: bool = False, order: int = 0) -> Any:
        if inspect.isfunction(cls):
            return self._register_function_bean(name, cls, primary=primary, aspect=aspect, order=order)
        if inspect.isclass(cls):
            return self._register_class_bean(name, cls, primary=primary, aspect=aspect, order=order)
        # 否则直接视为对象注册
        return self._register_class_object_bean(name, cls, primary=primary, aspect=aspect, order=order)

    def init(self):
        """初始化容器, 在bean都注册进工厂队列后执行, 同时解决多个容器间的依赖问题."""
        # 创建容器
        self._create_beans()
        # 初始化
        self._do_beans_init()
        self._initialized = True

    def _do_beans_init(self):
        # 对所有容器执行__post_construct__, InitializingBean.after_properties_set 初始化方法
        for beans in self._name_bean.values():
            for bean in beans:
                if bean.ioc_initialized:
                  continue
                # 容器原始类型是类才能执行
                if inspect.isclass(bean.ioc_type()):
                    if hasattr(bean.ioc_type(), '__post_construct__'):
                        bean.__post_construct__()
                        bean.ioc_initialized = True
                    if issubclass(bean.ioc_type(), InitializingBean):
                        bean.after_properties_set()
                        bean.ioc_initialized = True

    def _create_beans(self):
        depends = []
        # 优先创建无依赖的bean
        while True:
            try:
                order, param = self._init_queue.get(block=False)
                # 没有依赖则可以直接注册bean
                depends_params, depends_name_params = self._get_depends_args(param)
                if not depends_params:
                    self._register_bean(param.name, param.cls, param.primary, param.aspect, param.order)
                    continue
                # 依赖入队列
                depends.append({'param': param, 'depends': depends_params, 'depends_name': depends_name_params})
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
                name_map = dep.get('depends_name') or {}
                for name, cls in dep['depends'].items():
                    # 获取依赖bean实例
                    bean_name = name_map.get(name)
                    if bean_name:
                        obj = self.get_bean(name=bean_name, required_type=cls)
                    else:
                        obj = self.get_bean(name=name, required_type=cls) or self.get_bean(required_type=cls)
                    # 依赖bean不存在则跳过处理下一个
                    if obj is None:
                        break
                    params[name] = obj
                # 获取的依赖数量与目标一致则可以创建bean
                if len(params) == len(dep['depends']):
                    self._register_bean(dep['param'].name, dep['param'].cls, dep['param'].primary, dep['param'].aspect,
                                        dep['param'].order)
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
            self._register_bean(dep['param'].name, dep['param'].cls, dep['param'].primary, dep['param'].aspect,
                                dep['param'].order)

    def _get_depends_args(self, param: _Param) -> Tuple[Optional[dict], Optional[dict]]:
        """判断要创建的bean是否存在依赖
        """
        name, cls, primary = param.name, param.cls, param.primary
        if inspect.isclass(cls):
            # 属性Autowired依赖
            args, name_args = self._extract_class_attr_depends_args(cls)
            # 构造函数依赖
            f_args, f_name_args = self._extract_fun_depends_args(cls)
            args.update(f_args)
            name_args.update(f_name_args)
            return args, name_args
        if inspect.isfunction(cls):
            return self._extract_fun_depends_args(cls)
        # 对象注入无需依赖
        return None, None

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

    def _rebuild_bean_from_aspect(self, aspect):
        for k, v in self._type_bean.items():
            self._type_bean[k] = [AspectClassBeanProxy(e.ioc_name(), e, SelectorAspect(aspect)) for e in v if e not in self._aspect_bean]
        for k, v in self._name_bean.items():
            self._name_bean[k] = [AspectClassBeanProxy(e.ioc_name(), e, SelectorAspect(aspect)) for e in v if e not in self._aspect_bean]

    def _build_bean_by_aspects(self, proxy):
        for bean in self._aspect_bean:
            proxy = AspectClassBeanProxy(proxy.ioc_name(), proxy, SelectorAspect(bean))
        return proxy
