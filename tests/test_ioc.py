import dataclasses
import inspect
import json
import uuid

from seatools import ioc
from seatools.ioc.beans.factory import InitializingBean
from seatools.ioc.config import load_config, cfg


@ioc.Bean  # 默认name会转为小驼峰 randomUuidFunc
def random_uuid_func():
    return uuid.uuid4


@ioc.Bean
def int_bean():
    return 1


@ioc.Bean
class A:
    def __init__(self, uuid_func=ioc.Autowired(value='randomUuidFunc')):
        # 不支持在init中操作uuid_func依赖注入对象
        self._uuid_func = uuid_func
        self._uuid = None

    def __post_construct__(self):
        self._uuid = self._uuid_func()
        print('A.__post_construct__被执行, uuid=', self._uuid)

    def data(self):
        return self._uuid


@ioc.Bean(name='a2', primary=True)
def a():
    return A()


@ioc.Bean
class B(InitializingBean):
    def after_properties_set(self):
        print('B.after_properties_set被执行, a.data() = ', self._a.data())

    def __init__(self, a: A = ioc.Autowired(cls=A)):
        self._a = a

    def data(self):
        return 'B delay {}'.format(self._a.data())


@ioc.Bean
class C:
    a: int
    b: int
    c: str

    def __init__(self, a=ioc.Value('${c.a}'),
                 b=ioc.Value('${c.b}'),
                 c=ioc.Value('${c.c}', default_value=None),
                 ):
        self.a = a
        self.b = b
        self.c = c


def test_ioc():
    # 启动ioc, 扫描当期tests包
    ioc.run(scan_package_names='tests.test_ioc', config_dir='config')
    context = ioc.get_application_context()
    v = context.get_bean_by_name('intBean')
    print(v.get())
    a = context.get_bean_by_name('a')
    print(a.data())
    b = context.get_bean_by_type(B)
    print(b.data())
    v = context.get_bean_by_type(int)
    print(v == 1)
    c = context.get_bean('c')
    print(c)
