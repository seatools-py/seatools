from sqlalchemy import text
from sqlalchemy.orm import Session

from seatools.ioc import Bean, run
from seatools.ioc.database import DatabaseConfig
from seatools.sqlalchemy import SqlAlchemyClient
from seatools.ioc.sqlalchemy import new_session


def test_ioc_database():
    cfg = DatabaseConfig(
        host='localhost',
        port=6379,
        password='123456',
        database=0,
        driver='redis'
    )
    print(cfg.render_to_string())
    print(cfg.render_to_string(False))


@Bean
def sqlalchemy_client() -> SqlAlchemyClient:
    return SqlAlchemyClient(
        url='sqlite:///test.db'
    )


@new_session(autocommit=False)
def handler(session: Session):
    ans = session.execute(text('select 2')).scalars().first()
    assert ans == 2


def test_sqlalchemy():
    run(scan_package_names=['tests.test_ioc_database'])

    handler()
