from typing import Union, List

from .base import DataFileLoader, DataFileExtractor


class EvalDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       **kwargs) -> Union[dict, tuple, list]:
        return eval(config_data)


class EvalDataFileExtractor(DataFileExtractor):

    def _convert_data_to_str(self, data: Union[dict, List[dict]], **kwargs) -> str:
        raise NotImplementedError('不支持当前类型文件提取')

