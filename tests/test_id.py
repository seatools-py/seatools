from seatools.id import Snowflake
from loguru import logger

def test_snowflake():
    s = Snowflake()
    for i in range(20):
        logger.success(s.next_id())

