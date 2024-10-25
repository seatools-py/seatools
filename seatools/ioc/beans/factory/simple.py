import inspect
import queue
from typing import Any, Type, Callable, Union

from seatools.ioc.beans.proxy import *
from seatools.ioc.utils import class_utils
from .base import BeanFactory
from .initializing_bean import InitializingBean

from seatools.ioc.utils.name_utils import to_camel_case


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
        self._register_class_object_bean(name=self.__class__.__name__, obj=self)

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
                [bean for bean in beans if class_utils.is_family_type(bean.ioc_type(), required_type)])
            if bean:
                return bean
        return self._resolve_bean_from_beans(beans)

    def _resolve_type_bean(self, required_type=None):
        beans = self._type_bean.get(required_type)
        if not beans:
            beans = []
            for _type in self._type_bean.keys():
                if class_utils.is_family_type(_type, required_type):
                    beans = [*beans, *self._type_bean[_type]]
        return self._resolve_bean_from_beans(beans)

    def _register_function_bean(self, name: str, func, primary: bool = False) -> Any:
        name = name or to_camel_case(func.__name__, upper_case=False)
        proxy = ClassBeanProxy(name=name, obj=func(), primary=primary)
        self._add_bean(proxy.ioc_name(), proxy.ioc_type(), proxy)
        return proxy

    def _register_class_object_bean(self, name, obj, primary: bool = False) -> Any:
        name = name or to_camel_case(obj.__class__.__name__, upper_case=False)
        proxy = ClassBeanProxy(name=name, obj=obj, primary=primary)
        self._add_bean(proxy.ioc_name(), proxy.ioc_type(), proxy)
        return proxy

    def _register_class_bean(self, name: str, cls, primary: bool = False) -> Any:
        return self._register_class_object_bean(name, cls(), primary=primary)

    def register_bean(self, name: str, cls, primary: bool = False, lazy=True) -> Any:
        # 注册bean懒加载, 在init方法执行bean创建逻辑
        if lazy:
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
        while True:
            try:
                param: _Param = self._init_queue.get(block=False)
                # 没有依赖则可以直接注册bean
                if not self._has_dependency(param):
                    self._register_bean(param.name, param.cls, param.primary)
                    continue
                # todo: 依赖处理策略
            except queue.Empty:
                break

    def _has_dependency(self, param: _Param) -> bool:
        """判断要创建的bean是否存在依赖
        """
        # todo: 逻辑待实现
        return False

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
