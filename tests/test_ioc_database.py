from seatools.ioc.database import DatabaseConfig

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
