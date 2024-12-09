import pytest
from seatools.impala.impyla import ImpylaClient
from loguru import logger
from seatools.models import BaseModel
import datetime
from typing import Optional


class TestModel(BaseModel):
    id: int
    name: str
    desc: str
    create_time: datetime.datetime
    update_time: Optional[datetime.datetime] = None


@pytest.mark.skip()
def test_impyla():
    client = ImpylaClient(host='localhost', port=21050,
                          user='root',
                          database='test_db')
    ans = client.execute("""
SELECT *
FROM test
limit 10;
""")
    logger.info(ans)
    ans = client.execute("""
    SELECT *
    FROM test
    limit 10;
    """, modelclass=TestModel)
    logger.info(ans)
