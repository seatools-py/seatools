import queue
import threading
from seatools.ioc.beans.factory import BeanFactory
from seatools.ioc.context import ApplicationContext
from seatools.ioc.environment import Environment

_lock = threading.RLock()
# 该队列用来解决在bean factory创建之前就执行注入的内容
_pre_inject_queue = queue.Queue()


class _BeanVars:
    bean_factory: BeanFactory = None
    application_context = None
    environment = None


def new_bean_factory(factory=None):
    with _lock:
        if factory:
            _BeanVars.bean_factory = factory
        else:
            from seatools.ioc.beans.factory import SimpleBeanFactory
            _BeanVars.bean_factory = SimpleBeanFactory()
    _consume_pre_inject_queue()
    return _BeanVars.bean_factory


def get_bean_factory():
    return _BeanVars.bean_factory


def get_application_context() -> ApplicationContext:
    if _BeanVars.application_context:
        return _BeanVars.application_context
    with _lock:
        _BeanVars.application_context = ApplicationContext(bean_factory=_BeanVars.bean_factory)
    return _BeanVars.application_context


def get_environment() -> Environment:
    if _BeanVars.environment:
        return _BeanVars.environment
    with _lock:
        context = get_application_context()
        _BeanVars.environment = context.get_bean(name='environment', cls=Environment)
    return _BeanVars.environment


def _get_bean_factory():
    return _BeanVars.bean_factory


def _register_bean(**kwargs):
    """注册bean"""
    # 如果bean工厂已经创建, 则直接注入
    if _BeanVars.bean_factory:
        _BeanVars.bean_factory.register_bean(**kwargs)
        return
    # bean工厂不存在, 则放入队列
    _pre_inject_queue.put(kwargs)


def _consume_pre_inject_queue():
    """消费注入函数队列"""
    while True:
        try:
            kwargs = _pre_inject_queue.get(block=False)
            _BeanVars.bean_factory.register_bean(**kwargs)
        except queue.Empty:
            break
