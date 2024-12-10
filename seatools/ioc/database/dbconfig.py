from typing import Optional
from urllib.parse import quote, quote_plus
from seatools.models import BaseModel


class DatabaseConfig(BaseModel):
    """通用 DB 配置"""
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    # 是否是ioc primary实例
    primary: Optional[bool] = False
    # 数据库驱动
    driver: Optional[str] = None
    query: Optional[dict] = None

    def render_to_string(self, hide_password: bool = True):
        if self.driver is None:
            raise ValueError("Driver must be set.")
        s = self.driver + '://'
        if self.user is not None or self.password is not None:
            if self.user is not None:
                s += quote(self.user, safe=' +')
            if self.password is not None:
                s += ':' + ('***' if hide_password else quote(self.password, safe=' +'))
            s += '@'
        if self.host is not None:
            if ":" in self.host:
                s += f"[{self.host}]"
            else:
                s += self.host
        if self.port is not None:
            s += ":" + str(self.port)
        if self.database is not None:
            s += "/" + self.database
        if self.query:
            s += "?" + "&".join(
                f"{quote_plus(k)}={quote_plus(element)}"
                for k, element in self.query.items()
            )
        return s

