### `seatools.models` pydantic Model 封装
1. `seatools.models.BaseModel` - `class`: 对`pydantic.BaseModel`进行的拓展, 建议使用该Model或拓展该Model作为基础Model

示例:

```python
from seatools.models import BaseModel
import datetime


class AModel(BaseModel):
    a: int
    b: datetime.datetime


# a = AModel(a=1 b=datetime.datetime(2023, 12, 31, 0, 0, 23))
a = AModel(a=1, b='2023-12-31 00:00:23')
print(a)
```
2. `seatools.models.R` - `class`: 通用交互响应封装, 可用于web, rpc, websocket等交互式业务中的响应基础Model, 示例如下:

```python
from seatools.models import R

web_ok_response = R.ok(data='xxxx')
web_ok_response = R.ok(data='xxxx', msg='请求成功')
web_ok_response = R.ok(data='xxxx', msg='请求成功', code=200)

web_fail_response = R.fail('操作失败')
web_fail_response = R.fail('操作失败', code=500)
```
3. `seatools.models.PageModel`, `seatools.models.PageR` - `class`: 通用分页交互响应封装, 可用于web, rpc, websocket等交互式业务中的响应基础Model, `PageModel`还可作为分页请求基础Model, 示例如下:

```python
from seatools.models import PageR, PageModel

page_response = PageR.ok(PageModel(rows=['1234'], total=1))


# 模拟封装业务分页请求Model, 以用户名模糊查询分页查询请求示例, 此处PageModel作为基础Model
class BizReq(PageModel):
    user_name: str


# 模拟业务分页请求Model
biz_request = BizReq(page=1, page_size=10, user_name='xxx')
# 模拟业务分页响应
# ...模拟处理逻辑
biz_model = PageModel(page=biz_request.page,
                      page_size=biz_request.page_size,
                      rows=[{'a': 1, 'user_name': 'xxx'}],
                      total=1)
biz_response = PageR.ok(data=biz_model)
```
