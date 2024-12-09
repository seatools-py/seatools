import pytest
from seatools.models import BaseModel
from seatools.clickhouse.clickhouse_driver import ClickhouseDriverClient
from loguru import logger


class TestPythonTblModel(BaseModel):
    id: int
    name: str


def get_client():
    return ClickhouseDriverClient(
        host="localhost",
        port=9000,
        database="test",
        user="root",
        password="123456"
    )


@pytest.mark.skip()
def test_clickhouse_driver():
    client = get_client()
    client.execute('insert into test_python_tbl(`id`, `name`) values(1, \'测试名称\')')
    res = client.execute('select * from test_python_tbl limit 10', modelclass=TestPythonTblModel)
    logger.info(res)
