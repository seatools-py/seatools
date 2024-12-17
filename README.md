# Seatools Python新一代IOC框架 (Python >= 3.9)


## 仓库地址:
1. https://github.com/seatools-py/seatools
2. https://gitee.com/seatools-py/seatools

## Cookiecutter-seatools-python 模板项目地址
1. https://github.com/seatools-py/cookiecutter-seatools-python
2. https://gitee.com/seatools-py/cookiecutter-seatools-python

启动器列表地址具体见：[https://gitee.com/seatools-py](https://gitee.com/seatools-py)

## 联系方式, qq: 521274311 邮箱: 521274311@qq.com

## 安装
```shell
pip install seatools --upgrade
```

## 介绍

Seatools 参考 Java Spring 独立设计一套相似 API 的轻量级 IOC 工具，对 Java Spring 熟悉的开发者能够快速上手

## 实现原理
1. 与Java Spring类似通过包模块扫描，将需要IOC创建管理容器的配置信息放入队列，在IOC初始化完成后，将队列中的容器配置全部取出依次生成容器
2. Autowired, Value均通过代理对象+懒加载实现，在运行过程中需要用到容器时才从ioc中取出容器，从而避免循环依赖问题，其中自动注入依赖容器也通过Autowired的懒加载实现
3. 由于Value是代理对象的原因，Python解释器在对基本数据类型做常见运算/操作，例如数值类型的`+`,`-`,`*`,`/`，字符串的`+`等，会对类型做校验从而导致异常, 针对基本数据类型, Value提供一套基本类型转换属性来规避该问题, 例如存在配置a: 1，使用Value时使用该方式获取int类型的数据类型来完成计算`Value('${a}').int + 2`

## 使用场景
1. 复杂依赖场景 (含循环依赖)
2. 需要解耦灵活调整抽象实现场景,假设业务顶级包名为`xxx`, 以下为代码示例：

```python
"""
xxx/service.py
"""
import abc


class XXXService(abc.ABC):

    def do_anything(self):
        raise NotImplementedError


"""
xxx/service_impl.py
"""
class XXXAService(XXXService):

    def do_anything(self):
        print("XXXA")


class XXXBService(XXXAService):

    def do_anything(self):
        print("XXXB")

"""
xxx/config.py
"""
from seatools.ioc import Bean

@Bean(primary=True)
def new_xxxa_service(): # 涉及依赖可写在方法参数里
    return XXXAService()


@Bean(name='xxxb')
def new_xxxb_service():
    return XXXBService()

"""
xxx/main.py
"""
from seatools.ioc import run, Autowired

# 启动ioc依赖
run(scan_package_names='xxx', config_dir='./config')

xxxa = Autowired(cls=XXXService) # 由于XXXService有XXXAService和XXXBService两个子类, 并且均定义了IOC容器实例, 当仅传递类型时, 会自动扫描获取primary=True的Bean返回
xxxa.do_anything() # 输出：XXXA
xxxb = Autowired('xxxb', cls=XXXService) # 通过名称+类型获取 XXXBService IOC 容器实例
xxxb.do_anything() # 输出：XXXB

"""
一些建议：
在需要解耦灵活调整抽象实现场景下，通常我们可直接通过Autowired(cls=抽象类型)来获取该类型的实例，而具体抽象类型实现的Bean我们可以在ioc配置的python文件中定义需要用到的子类型实例容器，从而实现在不修改逻辑的情况下动态修改实现
"""
```

## IOC 工具
1. `seatools.ioc.boot.run` - `function`: ioc 启动函数, 类似 Java Spring 的 `@SpringBootApplication`，需要声明扫描的包与配置目录, 目前默认读取配置目录的`application.yml`,`application-[dev|test|pro].yml` 后续会拓展文件类型, 使用示例:
```python
from seatools.ioc import run
run(scan_package_names='xxx', config_dir='config') # 其中scan_package_names参数支持字符串, 字符串列表, 按顺序扫描包
```

2. `seatools.ioc.Bean` - `decorator`: ioc 容器装饰器, 支持装饰[类型, 方法]，类似 Java Spring 的 `@Bean`，使用示例如下：
```python
from seatools.ioc import run, Bean

"""
@Bean: 为类A创建一个容器实例并由ioc管理
支持参数如下:
  name: bean名称, 不填默认小写驼峰名称, 与java spring一致
  primary: 是否为该类型的默认bean, 不填默认否false, 与java spring @Primary 效果一致
"""
@Bean
class A:
    ...

run(scan_package_names='xxx', config_dir='config')
```

3. `seatools.ioc.Autowired` - `class`: ioc 容器自动注入类型, 与 Java Spring 的 `@Autowired` 类似，使用示例如下：
```python
from seatools.ioc import run, Bean, Autowired

"""
@Bean: 为类A创建一个容器实例并由ioc管理
支持参数如下:
  name: bean名称, 不填默认小写驼峰名称, 与java spring一致
  primary: 是否为该类型的默认bean, 不填默认否false, 与java spring @Primary 效果一致
"""
@Bean
class A:
    def hello():
        print('this is A.')

run(scan_package_names='xxx', config_dir='config')

"""
Autowired: 自动注入容器
支持参数如下:
  value: bean名称, 填入该值会基于名称获取
  cls: bean类型, 填入该值会基于类型获取, 若同时填入value则会两个条件同时查找
  required: 是否强制要求获取容器, 为True时无法获取容器则会抛出ValueError（后续改为其他异常，会异常ValueError）,为False找不到容器时会默认返回None
"""
# 从IOC容器中获取A实例
a = Autowired(cls=A) # 基于容器类型获取
a2 = Autowired('a') # 基于容器名称获取
a.hello()
"""
输出: this is A.
"""
print(a == a2) # 返回 True

# 也支持方法创建Bean
@Bean(name='a2')
def a2():
    return A()
```

4. `seatools.ioc.Value` - `class`: ioc 配置自动装载类型, 类似 Java Spring 的 `@Value`, 使用示例如下:
```python
"""
config/application.yml 配置文件如下
a: 1
b: x
c:
  a: 2
  b: y
"""
from seatools.ioc import run, Value

run(scan_package_names='xxx', config_dir='config')

a = Value('${a}') # 属性需要使用${}包裹, 该处为获取a配置的值即1
# 需要注意：Value获取基本数据类型, 无法直接使用, 需要使用对应类型的属性才可使用, 示例如下:
print(a.int + 5)
"""
输出: 6
"""
b = Value('${b}')
print(b.str + 'aa')
"""
输出: xaa
"""

# Value也允许直接装配Model
from seatools.models import BaseModel

class C(BaseModel):
    a: int
    b: str

class Config(BaseModel):
    a: int
    b: str
    c: C

# Value获取的model每次都是一个新的对象, 若获取的对象无需操作, 建议只获取一次即可
c = Value('${c}', cls=C)
print(c.a, c.b)
"""
输出: 2 y
"""

config = Value('${}', cls=Config)
print(config.a, config.b, config.c.a, config.c.b)
"""
输出 1 x 2 y
"""
```

5. `seatools.ioc.ConfigurationPropertiesBean` - `decorator`: ioc 的配置属性自动装配bean实例装饰器, 类似 Java Spring 的 `@ConfigurationProperties + @Bean` 的组合, 使用示例如下:
```python
"""
config/application.yml 配置文件如下
a: 1
b: x
c:
  a: 2
  b: y
"""
from typing import Optional
from seatools.ioc import run, ConfigurationPropertiesBean, Autowired
from seatools.models import BaseModel


@ConfigurationPropertiesBean(prop='c')
class C(BaseModel):
    a: int
    b: str


@ConfigurationPropertiesBean()
class Config(BaseModel):
    a: int
    b: str
    c: C

run(scan_package_names='xxx', config_dir='config')

c = Autowired(cls=C)
print(c.a, c.b)
"""
输出: 2 y
"""
config = Autowired(cls=Config)
print(config.a, config.b, config.c.a, config.c.b)
"""
输出 1 x 2 y
"""

# 也支持方法创建Bean
class Config2(BaseModel):
    a: Optional[int] = None
    b: Optional[str] = None
    c: Optional[C] = None

@ConfigurationPropertiesBean()
def config2():
    return Config2()
```

6. `seatools.ioc.beans.factory.InitializingBean` - `abstract class`: 初始化bean后的后置方法, 可在bean初始化属性完成后执行额外操作, 与 Java Spring `InitializingBean` 类似, 使用示例:
```python
from seatools.ioc import run, Autowired, Bean
from seatools.ioc.beans.factory import InitializingBean


@Bean
class A(InitializingBean):

    def after_properties_set(self):
       print('initializaing A')

    def hello(self):
        print('hello A')


run(scan_package_names='xxx', config_dir='config')

a = Autowired(cls=A)
a.hello()

"""
输出:
initializaing A
hello A
"""
```

7. 依赖自动注入示例：
```python
"""
config/application.yml 配置文件如下
a: 1
b: x
c:
  a: 2
  b: y
"""
from seatools.models import BaseModel
from seatools.ioc import run, Autowired, Bean, ConfigurationPropertiesBean


class C(BaseModel):
    a: int
    b: str


@ConfigurationPropertiesBean()
class Config(BaseModel):
    a: int
    b: str
    c: C


@Bean
class XXXService:

    def __init__(self, config: Config): # 必填参数会自动装配, 有默认值不会自动装配, 若想通过默认值自动装配, 可写为 def __init__(self, config = Autowired(cls=Config)):
        self._config = config

    def print(self):
        print(self._config)


run(scan_package_names='xxx', config_dir='config')

xxx_service = Autowired(cls=XXXService)
xxx_service.print()
"""
输出: a=1 y='x' c=C(a=2, b='y')
"""
```



## 核心 APIs 列表
### [一、`seatools.ioc` 轻量级ioc工具](./docs/ioc工具.md), [ioc详解](./docs/ioc详解.md)

## 工具 APIs 列表
### [二. `seatools.builders` 特定格式内容建造器, 例如: html标签, markdown语法等](./docs/Html、Markdown建造器.md)
### [三. `seatools.files` 文件/文件类型数据处理工具, 例如: json, csv, yaml, ini等](./docs/文件或文件类型数据处理工具.md)
### [四. `seatools.models` pydantic Model 封装等, 墙裂推荐, 业务上均应该使用pydantic](./docs/pydantic封装.md)
### [五. `seatools.notices` 通知工具, 例如: 飞书通知、邮箱通知等](./docs/通知工具.md)
### [六. `seatools.cryptography` 常用加密解密包, 例如: md5, base64, hmac等](./docs/常用加密解密工具.md)
### [七、`seatools.env` 多环境管理工具包, 例如: 开发环境、测试环境、正式环境等](./docs/多环境工具包.md)
### [八、`seatools.sqlalchemy` sqlalchemy ORM工具包](./docs/sqlalchemy工具包.md)
### [九、`seatools.retry` 重试工具](./docs/重试工具.md)
### [十、`seatools.task` 任务工具](./docs/任务工具.md)
### [十一、`seatools.cache` 缓存工具](./docs/缓存工具.md)
### [十二. `seatools.logger` 日志工具包(通过setup方法设置日志文件+loguru框架记录日志)](./docs/日志工具包.md)
### [十三、`seatools.redis_om` redis-om拓展](./docs/redis-om拓展.md)
### [十四、`seatools.uc` undetected-chromedriver拓展工具](./docs/undetected-chromedriver拓展工具.md)
