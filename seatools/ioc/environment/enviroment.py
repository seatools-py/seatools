from typing import Type, Dict, Any
from seatools.ioc.config import cfg
from seatools.ioc.utils.value_utils import convert


class Environment:

    def get_property(self, name: str, cls: Type = None) -> Any:
        if not name:
            raise ValueError('Environment name不能为空')
        data = self._parse_config_value(data=cfg(), config_name_path=name)
        if data is None:
            return None
        if cls:
            return convert(data, cls)
        return data

    def _parse_config_value(self, data: Dict, config_name_path: str):
        config_names = config_name_path.split('.')
        current = dict(data)
        for i, config_name in enumerate(config_names):
            if not isinstance(current, dict):
                return None
            if '[' in config_name:
                index_key, index_value = config_name.split('[')
                index_value = index_value.rstrip(']')
                current = current.get(index_key)
                if current is None:
                    return None
                if not isinstance(current, list):
                    return None
                if index_value >= len(current):
                    return None
                current = current[index_value]
            else:
                current = current.get(config_name)
        return current
