from typing import Union, List

from .base import DataFileLoader, DataFileExtractor


class CsvDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       header=False,
                                       use_header_as_key=False,
                                       **kwargs) -> Union[dict, tuple, list]:
        """
        Args:
            header: 是否第一行为csv表格头
            use_header_as_key: 是否将header头作为key, 仅header = True生效
        """
        if isinstance(config_data, bytes):
            config_data = config_data.decode('utf-8')
        config_data = config_data.split('\n')
        keys = None
        if header:
            if len(config_data) <= 1:
                return []
            if use_header_as_key:
                keys = config_data[0].split(',')
            config_data = config_data[1:]
        if len(config_data) <= 0:
            return []
        result = []
        for config_data_item in config_data:
            if not config_data_item:
                continue
            config_data_item = config_data_item.split(',')
            if keys:
                item = {}
            else:
                item = []
            for i in range(len(config_data_item)):
                if keys:
                    item[keys[i]] = config_data_item[i]
                else:
                    item.append(config_data_item[i])
            result.append(item)
        return result


class CsvDataFileExtractor(DataFileExtractor):

    def _convert_data_to_str(self, data: Union[dict, List[dict]],
                             header=True,
                             **kwargs):
        if isinstance(data, dict):
            data = [data]
        keys = list(set(*[item.keys() for item in data]))
        keys.sort()
        ans = ''
        if header:
            for k in keys:
                if ans:
                    ans += ','
                ans += k
            ans += '\n'
        for v in data:
            line = ''
            for k in keys:
                if line:
                    line += ','
                line += self._extract_value(v.get(k))
            ans += line + '\n'
        return ans
