from typing import Type, Any, List
from seatools.ioc.config import cfg
from seatools.ioc.utils.value_utils import convert, parse_express_value


class Environment:

    def __init__(self):
        self._active_profiles = None

    def get_property(self, name: str, cls: Type = None) -> Any:
        data = parse_express_value(data=cfg(), express=name)
        if data is None:
            if cls:
                return cls()
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
