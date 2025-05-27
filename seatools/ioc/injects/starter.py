import inspect
import os
from typing import Union, List

from seatools.ioc import run
from seatools.ioc.beans.factory import BeanFactory


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
