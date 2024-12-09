from typing import Union, List, Any

from .base import DataFileLoader, DataFileExtractor


def _load_properties_data(config_data: str):
    def dfs_properties_key(p, keys, value):
        if len(keys) == 1:
            p[keys[0]] = value
            return
        if keys[0] not in p:
            p[keys[0]] = {}
        dfs_properties_key(p[keys[0]], keys[1:], value)

    properties = {}
    for line in config_data.split('\n'):
        if not line.strip() or line.startswith('#'):
            continue
        if '=' not in line:
            raise ValueError('properties文件格式错误, 每一行必须包含"=".')
        key, value = line.split('=', 1)
        key, value = key.strip(), value.strip()
        keys = key.split(".")
        if len(keys) >= 2:
            dfs_properties_key(properties, keys, value)
        else:
            properties[key] = value

    return properties


class PropertiesDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       encoding: str = 'utf-8',
                                       **kwargs) -> Union[dict, tuple, list]:
        if isinstance(config_data, bytes):
            config_data = config_data.decode(encoding=encoding)
        return _load_properties_data(config_data)


class PropertiesDataFileExtractor(DataFileExtractor):

    def _convert_data_to_str(self, data: Union[dict, List[dict]], **kwargs):
        return '\n'.join(self._parse_property(data))

    def _parse_property(self, data: Any, prefix=''):
        def parse_key(key=None, index=None, prefix=''):
            if index is not None:
                if prefix:
                    return '{}[{}]'.format(prefix, index)
                return '[{}]'.format(index)
            if key and prefix:
                return '{}.{}'.format(prefix, key)
            return key or ''

        ans = []
        if isinstance(data, dict):
            for key, value in data.items():
                ans = [*ans, *(self._parse_property(value, prefix=parse_key(key, None, prefix)))]
            return ans
        if isinstance(data, list):
            for index, item in enumerate(data):
                ans = [*ans, *(self._parse_property(item, prefix=parse_key(None, index, prefix)))]
            return ans
        return ['{}={}'.format(prefix, self._extract_value(data))]
