from loguru import logger as log
from typing import Union, List

from .base import DataFileLoader, DataFileExtractor


class YamlDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       **kwargs) -> Union[dict, tuple, list]:
        try:
            import yaml
            return yaml.safe_load(config_data)
        except ImportError as e:
            log.warning('未安装pyyaml模块, 无法解析yaml格式数据')
            raise e


class YamlDataFileExtractor(DataFileExtractor):

    def _convert_data_to_str(self, data: Union[dict, List[dict]],
                             **kwargs):
        try:
            import yaml
            return yaml.dump(data)
        except ImportError as e:
            log.warning('未安装pyyaml模块, 无法解析yaml格式数据')
            raise e
