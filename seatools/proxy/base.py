import uuid
from abc import ABC, abstractmethod
from seatools.models import BaseModel
from contextlib import contextmanager
from typing import Any, TypeVar


class ProxyInfo(BaseModel):
    """代理信息"""
    # 代理ID, 与IP或者上线文关联, 业务自己实现, 例如uuid等
    proxy_id: str
    # 代理信息, 具体由业务决定, 例如http代理需要包含http代理的url(有些还需要账号密码, 加密等参数)
    info: Any


_PROXY_INFO = TypeVar('_PROXY_INFO', bound=ProxyInfo)


class ProxyPool(ABC):
    """代理池抽象封装"""

    def __init__(self):
        self._proxy_map = {}

    def acquire(self, proxy_id: str) -> _PROXY_INFO:
        """获取一个代理信息, 若第一次获取则从池中生成一个代理

        Args:
            proxy_id: 代理ID

        Returns:
            代理信息
        """
        proxy_info = self._proxy_map.get(proxy_id)
        if proxy_info and not self.check_proxy_expired(proxy_id):
            return proxy_info
        proxy_info = self._gen_proxy_info()
        if proxy_info:
            self._proxy_map[proxy_id] = proxy_info
        return proxy_info

    def check_proxy_expired(self, proxy_id: str) -> bool:
        """检查代理是否已过期

        Args:
            proxy_id: 代理ID

        Returns:
            代理过期状态, true=已过期, false=未过期
        """
        proxy_info = self._proxy_map.get(proxy_id)
        if not proxy_info:
            return True
        return self._check_proxy_expired_impl(proxy_info)

    @abstractmethod
    def _check_proxy_expired_impl(self, proxy_info: _PROXY_INFO) -> bool:
        """检查代理是否过期

        Args:
            proxy_info: 代理信息

        Returns:
            代理过期状态, true=已过期, false=未过期
        """
        raise NotImplementedError

    def release(self, proxy_id: str):
        """释放一个代理, 将代理归还入池

        Args:
            proxy_id: 代理ID
        """
        if proxy_id in self._proxy_map:
            del self._proxy_map[proxy_id]

    @abstractmethod
    def _gen_proxy_info(self) -> _PROXY_INFO:
        """生成一个代理信息对象

        Returns:
            代理信息
        """
        raise NotImplementedError


class ProxyManager:
    """代理管理器"""

    def __init__(self, pool: ProxyPool):
        self._pool = pool

    @contextmanager
    def proxy(self) -> _PROXY_INFO:
        """获取一个代理

        使用示例:
            manager = ProxyManager(pool=xxx)
            with manager.proxy() as proxy_info:
                # 业务逻辑
                ...
        """
        proxy_id = str(uuid.uuid4())
        try:
            proxy_info = self._pool.acquire(proxy_id=proxy_id)
            yield proxy_info
        finally:
            self._pool.release(proxy_id=proxy_id)
