import importlib
import inspect
import os
from typing import List, Union
from threading import RLock

from loguru import logger

from seatools.ioc.context import ApplicationContext
from seatools.ioc.utils import reflect_utils
from seatools.ioc.base import new_bean_factory, get_bean_factory
from seatools.ioc.beans.factory import BeanFactory
from seatools.ioc.config import load_config


class _Properties:
    first = True
    lock = RLock()
    loaded_modules = set()


def run(scan_package_names: Union[List[str], str], config_dir: str = None, factory: BeanFactory = None,
        exclude_modules: List[str] = None, enable_aspect: bool = False):
    """Start seatools.ioc. Allow repeated runs. A module only load once.

    Args:
        scan_package_names: Packages to scan, supports multiple packages, e.g., xxx.xxx; xxx
        config_dir: Configuration directory, if not empty, it will load application.yml and application-{env}.yml files (if exist) from the config_dir directory into the system configuration.
        It also supports injecting properties and beans through IOC using @Value and @Configuration decorators.
        factory: Bean factory, can be implemented by yourself, defaults to SimpleBeanFactory.
        exclude_modules: List of modules to exclude.
        enable_aspect: Whether to enable AOP.
    """
    # Start with locking
    with _Properties.lock:
        if not scan_package_names:
            raise ValueError('Package name cannot be empty.')
        if isinstance(scan_package_names, str):
            scan_package_names = [scan_package_names]
        # Initialize factory
        if _Properties.first:
            bean_factory = new_bean_factory(factory=factory, enable_aspect=enable_aspect)
            # Initialize configuration if provided
            if config_dir:
                load_config(config_dir=config_dir)

            # Register Environment
            from seatools.ioc.environment import Environment
            bean_factory.register_bean(name='environment', cls=Environment, primary=True, lazy=False)

            # Register ApplicationContext
            bean_factory.register_bean(name='applicationContext', cls=ApplicationContext(bean_factory), primary=True,
                                       lazy=False)

            # Add starters package for priority auto-loading
            scan_package_names = ['seatools.ioc.starters'] + scan_package_names

            _Properties.first = False
        else:
            bean_factory = get_bean_factory()

        for scan_package_name in scan_package_names:
            # Load all beans in the package and inject into the factory
            modules = reflect_utils.get_all_py_modules(scan_package_name)
            for module in modules:
                if not exclude_modules:
                    _load_module(module)
                    continue
                for exclude_module in exclude_modules:
                    if module.startswith(exclude_module):
                        break
                else:
                    _load_module(module)
        # Bean initialization
        bean_factory.init()
        # Release loading resources
        _release()


def _release():
    # Release resources
    _Properties.loaded_modules.clear()


def _load_module(module):
    if module in _Properties.loaded_modules:
        return
    # Prevent infinite recursive loading, add to record first then loa
    _Properties.loaded_modules.add(module)
    try:
        importlib.import_module(module)
    except ModuleNotFoundError as e:
        logger.warning('Module {} not found.Cannot to import by seatools.ioc. Reason: {}', module, e)


def seatools_boot(*args,
                  scan_package_names: Union[List[str], str, None] = None,
                  config_dir: str = None,
                  factory: BeanFactory = None,
                  exclude_modules: List[str] = None):
    def wrapper(func):
        scans = scan_package_names
        module = inspect.getmodule(func)
        module_name = module.__name__ if module else None
        # 仅 __main__ 加载
        if module_name != '__main__':
            return func

        # 默认仅扫描当前模块
        if scans is None:
            file_path = inspect.getfile(func)
            current_module = file_path.split(os.sep)[-1].split('.')[0]
            scans = [current_module]

        # 启动IOC
        run(scan_package_names=scans,
            config_dir=config_dir,
            factory=factory,
            exclude_modules=exclude_modules)

        return func

    if len(args) == 1 and callable(*args):
        return wrapper(args[0])

    return wrapper


SeatoolsBoot = seatools_boot
