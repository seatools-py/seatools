from seatools.redis.dbconfig import RedisConfig
from seatools.redis.utils import new_redis


def test_redis():
    config = RedisConfig(
        host='localhost',
        port=6379,
        password='123456',
        database=0,
        config={'decode_responses': True}
    )
    client = new_redis(config, config.config)
    client.set('xxx', 1234)
    assert client.get('xxx') == '1234'

