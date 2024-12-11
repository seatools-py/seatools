import importlib
from typing import List, Union
from threading import RLock

from seatools.ioc.context import ApplicationContext
from seatools.ioc.utils import reflect_utils
from seatools.ioc.base import new_bean_factory
from seatools.ioc.beans.factory import BeanFactory
from seatools.ioc.config import load_config


class _Properties:
    running: int = 0
    lock = RLock()


def run(scan_package_names: Union[List[str], str], config_dir: str = None, factory: BeanFactory = None,
        exclude_modules: List[str] = None):
    """启动pyspring, 一个进程中重复启动仅第一次生效

    Args:
        scan_package_names: 需要扫描的包, 支持多个包, 示例: xxx.xxx; xxx
        config_dir: 配置目录, 若不为空则加将config_dir目录下的 application.yml, application-{env}.yml 文件(如果存在) 加载到系统配置中
        同时支持@Value, @Configuration装饰器通过IOC注入是属性和bean
        factory: bean工厂, 可自己实现, 默认走SimpleBeanFactory
        exclude_modules: 需要过滤的模块列表
    """
    # 启动加锁
    with _Properties.lock:
        if _Properties.running:
            return
        # 启动, 设置运行状态
        _Properties.running = 1
        if not scan_package_names:
            raise ValueError('包名不能为空')
        if isinstance(scan_package_names, str):
            scan_package_names = [scan_package_names]
        # 初始化工厂
        bean_factory = new_bean_factory(factory=factory)

        # 有配置则初始化配置
        if config_dir:
            load_config(config_dir=config_dir)

        # 注册Environment
        from seatools.ioc.environment import Environment
        bean_factory.register_bean(name='environment', cls=Environment, primary=True, lazy=False)

        # 注册 ApplicationContext
        bean_factory.register_bean(name='applicationContext', cls=ApplicationContext(bean_factory), primary=True,
                                   lazy=False)

        # 添加starters包优先自动加载
        scan_package_names = ['seatools.ioc.starters'] + scan_package_names

        for scan_package_name in scan_package_names:
            # 加载包下所有某个和bean, 并注入到工厂
            modules = reflect_utils.get_all_py_modules(scan_package_name)
            for module in modules:
                if exclude_modules and module in exclude_modules:
                    continue
                importlib.import_module(module)
        # 初始化创建bean实例
        bean_factory.init()

