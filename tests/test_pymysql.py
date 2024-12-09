import datetime
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import pytest

from seatools.mysql import pymysql
from seatools.models import BaseModel
from typing import Optional

pool = ThreadPoolExecutor(200)

SQL_DDL = """
CREATE TABLE `test_pymysql_tbl` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) NOT NULL COMMENT '名称',
  `is_delete` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '最近一次更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `test_pymysql_tbl_unique` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试pymysql表';
"""


class TestPyMysqlModel(BaseModel):
    id: int
    name: str
    is_delete: bool
    create_time: datetime.datetime
    update_time: Optional[datetime.datetime] = None


def save(conn: pymysql.Connection, sql):
    try:
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print('执行sql: ', sql, flush=True)
    except Exception:
        traceback.print_exc()


@pytest.mark.skip()
def test_pymysql():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        database='test_db',
    )
    for i in range(10000):
        pool.submit(save, conn, f"""
        insert into test_pymysql_tbl(name) values(test_pymysql_{time.time()})
        """)


@pytest.mark.skip()
def test_pymysql_helper():
    client = pymysql.PyMysqlClient(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        database='test_db',
    )
    sql = 'select * from test_pymysql_tbl limit 10'
    ans = client.execute(sql, modelclass=TestPyMysqlModel)
    print(ans)
    with client.transaction_client() as t_client:
        ans = t_client.execute(sql, modelclass=TestPyMysqlModel)
        print(ans)
