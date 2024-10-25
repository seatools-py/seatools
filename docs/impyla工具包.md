### `seatools.impala.impyla` impyla 工具包
1. `seatools.impala.impyla.ImpylaClient` - `class`: impyla 客户端封装, 使用示例如下:

```python
from seatools.models import BaseModel
from seatools.impala.impyla import ImpylaClient


class UserModel(BaseModel):
    id: int
    name: str


client = ImpylaClient(...)
# ans = [{'id': 1, 'name': '测试名称'}]
ans = client.execute('select * from user where id = %s', args=[1])
# ans = [UserModel(id=1, name='测试名称')]
ans = client.execute('select * from user where id = %s', args=[1], modelclass=UserModel)

```
