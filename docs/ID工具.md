### `seatools.id` ID工具包
1. `seatools.id.Snowflake` 雪花ID生成工具包(线程安全), 使用示例如下:
```python
from seatools.id import Snowflake

# 创建雪花ID生成工具
s = Snowflake(datacenter_id=1, worker_id=1)
# 获取雪花ID
snowflake_id = s.next_id()

```
