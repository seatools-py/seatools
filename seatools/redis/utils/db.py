from typing import Optional
from seatools.redis.dbconfig import RedisConfig


def new_redis(config: RedisConfig, extra_config: Optional[dict] = None):
    import redis
    url = config.render_to_string(hide_password=False)
    client = redis.Redis.from_url(url, **(extra_config or {}))
    return client
