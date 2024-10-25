### `seatools.mysql.pymysql` pymysql 工具包
1. `seatools.mysql.pymysql.PyMysqlHelper` - `class`: pymysql客户端工具类, 推荐使用, 使用示例

```python
from seatools.mysql.pymysql import PyMysqlClient
from seatools.models import BaseModel


class UserModel(BaseModel):
    id: int
    name: str


client = PyMysqlClient(...)
# 非事务sql
# ans = [{'id': 1, 'name': '测试名称'}]
ans = client.execute(sql='select * from user where id = %s', args=[1])
# 转换model, ans = [UserModel(id=1, name='测试名称')]
ans = client.execute(sql='select * from user where id = %s', args=[1], modelclass=UserModel)

# 事务模式, 在同一个cursor下执行多个sql保证事务一致性
with client.transaction_client() as t_client:
    # ans = [{'id': 1, 'name': '测试名称'}]
    ans = t_client.execute(sql='select * from user where id = %s', args=[1])
    # 转换model, ans = [UserModel(id=1, name='测试名称')]
    ans = t_client.execute(sql='select * from user where id = %s', args=[1], modelclass=UserModel)
```
2. `seatools.mysql.pymysql.connect` - `function`: 获取pymysql连接或pooldb池对象, 基础层方法, 不推荐使用!!!
