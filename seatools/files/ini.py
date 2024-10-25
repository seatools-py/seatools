from typing import Union, List

from .base import DataFileLoader, DataFileExtractor


class IniDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       encoding: str = 'utf-8',
                                       **kwargs) -> Union[dict, tuple, list]:
        if isinstance(config_data, bytes):
            config_data = config_data.decode(encoding=encoding)
        import configparser
        config = configparser.ConfigParser()
        config.read_string(config_data)
        config_dict = {section: dict(config.items(section))
                       for section in config.sections()}
        return config_dict


class IniDataFileExtractor(DataFileExtractor):

    def _convert_data_to_str(self, data: Union[dict, List[dict]], **kwargs) -> str:
        raise NotImplementedError('不支持当前类型文件提取')

