### `seatools.clickhouse.clickhouse_driver` clickhouse_driver 工具包
1. `seatools.clickhouse.clickhouse_driver.ClickhouseDriverClient` - `class`: clickhouse_driver 工具类, 使用方式如下

```python
from seatools.models import BaseModel
from seatools.clickhouse.clickhouse_driver import ClickhouseDriverClient


class UserModel(BaseModel):
    id: int
    name: str


client = ClickhouseDriverClient(...)
# ans = [{'id': 1, 'name': '测试名称'}]
ans = client.execute('select * from user where id = 1')
# ans = [UserModel(id=1, name='测试名称')]
ans = client.execute('select * from user where id = 1', modelclass=UserModel)
```
