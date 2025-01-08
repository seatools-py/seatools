import importlib.util
import inspect
from typing import Union, List, Type
from pydantic import BaseModel

from .base import DataFileLoader, DataFileExtractor


class PyDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       **kwargs) -> Union[dict, tuple, list]:
        return eval(config_data)

    def load_file(self,
                  file_path: str,
                  encoding: str = 'utf-8',
                  modelclass: Union[Type[dict], Type[BaseModel]] = dict,
                  **kwargs) -> Union[dict, list, BaseModel]:
        module_name = file_path.split('.')[0].replace('\\', '/').split('/')[-1]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        members = inspect.getmembers(module)

        data = {}

        for name, obj in members:
            if not inspect.isbuiltin(obj) and not inspect.ismodule(obj) and not name.startswith(
                '__') and not name.endswith('__'):
                data[name] = obj

        return self._convert_item_to_model(data, modelclass)


class PyDataFileExtractor(DataFileExtractor):

    def _convert_data_to_str(self, data: Union[dict, List[dict]], **kwargs) -> str:
        raise NotImplementedError('不支持当前类型文件提取')
