### `seatools.ioc` 轻量级IOC工具包, 类似spring语法

基本说明:
1. ioc 工具中的所有的bean均为代理对象, 代理对象代理了一系列方法与调用逻辑, 但是代理对象仍然不是原生类型, 针对py的基本数据类型或需要使用原始类型的场景, 请先获取bean然后调用bean.get()方法获取原始数据对象
2. ioc 依赖注入使用的代理对象+延迟注入机制实现, 请勿在构造函数, bean初始化方法中对依赖进行操作与调用, 若需要对依赖进行额外处理请在`__post_construct__`方法或继承`seatools.beans.factory.InitializingBean`类在`after_properties_set`方法中实现

基本功能:
1. `seatools.ioc.run` - `function`: ioc 启动方法, 扫描指定模块及所有子模块中的所有的bean, 注册进ioc容器中, 使用示例
```python
# xxxx.py

from seatools import ioc

# 扫描xxxx模块 (当前文件)
ioc.run(
    # 扫描的模块, 涉及 ioc 管理, 影响 Bean 装饰器及 Autowired 依赖注入
    scan_package_names='xxxx',
    # 配置目录, 默认加载 {config_dir}/application.yml, {config_dir}/application-dev.yml, {config_dir}/application-test.yml, {config_dir}/application-pro.yml
    # 涉及 Environment 管理, 影响 Value 配置注入
    config_dir='config',
)
```
2. `seatools.ioc.Bean` - `decorator`: Bean装饰器, 使用该装饰器将对象添加至 ioc 容器进行管理, 支持类与函数创建bean, 使用示例:
```python
# xxxx.py
from seatools import ioc

# 定义类ClassBean类型的一个ioc容器实例, 容器实例名称为cb
@ioc.Bean(name="cb")
class ClassBean:
    def hello(self):
        print('hello class bean')

class MethodBean:

    def hello(self):
        print('hello method bean')

# 定义类MethodBean类型的一个ioc容器实例, 容器实例名称为mb
@ioc.Bean(name="mb")
def new_method_bean():
    return MethodBean()

ioc.run(scan_package_names='xxxx')
ctx = ioc.get_application_context()
cb: ClassBean = ctx.get_bean(name='cb') # 等同于 ctx.get_bean_by_name('cb'), 也可通过类型获取 ctx.get_bean(cls=ClassBean) 或 ctx.get_bean_by_type(ClassBean)
cb.hello() # 输出 hello class bean
mb: MethodBean = ctx.get_bean_by_type(MethodBean)
mb.hello() # 输出 hello method bean
```
3. `seatools.ioc.Autowired` - `class`: 依赖注入, 使用示例:
```python
from seatools import ioc

@ioc.Bean(name='a')
class A:

    def hello(self):
        print('a')


# 类 bean 的依赖注入
@ioc.Bean(name='b')
class B:

    def __init__(self, a: A = ioc.Autowired(value='a')):
        self._a = a

    def hello(self):
        print('b')
        self._a.hello()


class C:

    def __init__(self, a: A):
        self._a = a

    def hello(self):
        print('c')
        self._a.hello()

# 方法 bean 的依赖注入
@ioc.Bean('c')
def new_c(a: A = ioc.Autowired(value='a')):
    return C(a=a)

ctx = ioc.get_application_context()
b: B = ctx.get_bean_by_name('b')
# 输出:
# b
# a
b.hello()

c: C = ctx.get_bean_by_type(C)
# 输出:
# c
# a
c.hello()
```
4. `seatools.ioc.get_application_context` - `function`: 获取 ioc 应用上下文对象, 通过应用上下文对象来获取容器实例, 使用实例:
```python
# xxxx.py
from seatools import ioc

@ioc.Bean
class A:
    def hello(self):
        print('hello A')

# 扫描xxxx模块 (当前文件)
ioc.run(scan_package_names='xxxx')
# 获取上下文对象
application_context = ioc.get_application_context()
# 通过名称获取, 默认名称为小驼峰, 即使下划线也会转为小驼峰, 更推荐在@ioc.Bean装饰器添加name参数, 示例: @ioc.Bean(name='a')
# 等同于 application_context.get_bean_by_name('a')
bean_a: A = application_context.get_bean(name='a')
# 通过类型获取
# 等同于 application_context.get_bean_by_type(A)
bean_a: A = application_context.get_bean(cls=A)

# 调用hello方法
bean_a.hello()
```
5. `seatools.ioc.Value` - `class` 配置注入, 使用示例:
```yaml
# config/application.yml
a:
  a: 1
```
```python
# xxxx.py
from seatools import ioc

@ioc.Bean
class A:

    def __init__(self,
                # 注入 config/application.yml中的a.a, 目前可拓展各种类型, 但必须以${}包裹配置, 不支持和其他字符串连接, 后续优化
                 a = ioc.Value(value='${a.a}', cls=int)):
        self._a = a

    def hello(self):
        print(f'hello {self._a.get()}')
ioc.run(scan_package_names='xxxx')
```
6. `seatools.beans.factory.InitializingBean` - `class` 或 `__post_construct__`: bean初始化额外逻辑, 若需要对所有依赖注入的对象在此处进行额外处理:

```python
# xxxx.py
from seatools import ioc
from seatools.ioc.beans.factory import InitializingBean


@ioc.Bean
class A:

    def gen_uuid(self):
        import uuid
        return str(uuid.uuid4())


@ioc.Bean
class B:

    def __init__(self, a: A = ioc.Autowired(cls=A)):
        # 注意此处不能直接写成 self._uuid = a.gen_uuid()
        self._uuid = None
        self._a = a

    def __post_construct__(self):
        self._uuid = self._a.gen_uuid()


@ioc.Bean
class C(InitializingBean):

    def __init__(self, a: A = ioc.Autowired(cls=A)):
        # 注意此处不能直接写成 self._uuid = a.gen_uuid()
        self._uuid = None
        self._a = a

    def after_properties_set(self):
        self._uuid = self._a.gen_uuid()

# 上述 B 和 C 实现是等效的
ioc.run(scan_package_names='xxxx')
```
7. `seatools.ioc.Environment` - `class`: ioc 管理的环境配置对象, 基于`ioc.run(..., config_dir="")`, 支持便捷的从配置中提取 `dict`, `pydantic model`, `dataclass`等结构数据, 使用示例:
```python
from seatools import ioc

ioc.run(scan_package_names='xxxx', config_dir='config')
environment = ioc.get_environment()
environment.get_property('a')
```
