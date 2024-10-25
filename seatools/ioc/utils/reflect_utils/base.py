import importlib
import os


def get_all_py_modules(package_or_module_name: str):
    """获取包下的所有py模块

    Args:
        package_or_module_name: 指定包名或模块
    """
    package_or_module = importlib.import_module(package_or_module_name)
    py_modules = []
    if hasattr(package_or_module, '__path__'):
        package_path = package_or_module.__path__[0]
        for root, _, files in os.walk(package_path):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    module_path = os.path.relpath(os.path.join(root, file), package_path)
                    module_name = os.path.splitext(module_path)[0].replace(os.path.sep, '.')
                    py_modules.append(f"{package_or_module_name}.{module_name}")
        return py_modules
    # 否则本身就是一个模块
    py_modules.append(package_or_module_name)
    return py_modules
