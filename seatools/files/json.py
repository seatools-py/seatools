import json
from typing import Union, List

from .base import DataFileLoader, DataFileExtractor


class JsonDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       **kwargs) -> Union[dict, tuple, list]:
        return json.loads(config_data)


class JsonDataFileExtractor(DataFileExtractor):

    def _convert_data_to_str(self, data: Union[dict, List[dict]],
                             **kwargs) -> str:
        return json.dumps(data, ensure_ascii=False)
