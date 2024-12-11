from typing import Type, Dict, Any, List
from seatools.ioc.config import cfg
from seatools.ioc.utils.value_utils import convert


class Environment:

    def __init__(self):
        self._active_profiles = None

    def get_property(self, name: str, cls: Type = None) -> Any:
        data = self._parse_config_value(data=cfg(), config_name_path=name)
        if data is None:
            return None
        if cls:
            return convert(data, cls)
        return data

    def get_active_profiles(self) -> List[str]:
        if not self._active_profiles:
            active_profiles = self.get_property("seatools.profiles.active")
            if not active_profiles:
                self._active_profiles = []
            else:
                self._active_profiles = [active_profile.strip() for active_profile in active_profiles.split(',')]
        return self._active_profiles

    def _parse_config_value(self, data: Dict, config_name_path: str):
        current = dict(data)
        if not config_name_path:
            return current
        config_names = config_name_path.split('.')
        for i, config_name in enumerate(config_names):
            if not isinstance(current, dict):
                return None
            if '[' in config_name:
                index_key, index_value = config_name.split('[')
                index_value = index_value.rstrip(']')
                index_value = int(index_value)
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
