import uuid

from seatools import ioc
from seatools.ioc import Autowired, Value
from seatools.ioc.beans.factory import InitializingBean
from seatools.models import BaseModel


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


class Cp(BaseModel):
    a: int
    b: int
    c: str

def test_ioc():
    # 启动ioc, 扫描当期tests包
    ioc.run(scan_package_names='tests.test_ioc', config_dir='config')
    context = ioc.get_application_context()
    v = Autowired('intBean')
    print(v)
    a = Autowired('a', cls=A)
    print(a.data())
    b = Autowired(cls=B)
    print(b.data())
    v = Autowired('intBean', cls=int)
    print(v.int == 1)
    c = Autowired(cls=C)
    print(c)
    print(Value('${a}').int)
    print(Value('${b}').int)
    c = Value('${c}', cls=Cp)
    print(c.c)


@ioc.Bean
class AA:

    def hello(self):
        print('hello AA')


@ioc.Bean
class BB:

    def __init__(self, aa: AA):
        self._aa = aa

    def hello(self):
        self._aa.hello()
        print('Hello BB')


def test_depends():
    ioc.run(scan_package_names='tests.test_ioc', config_dir='config')
    b: BB = ioc.Autowired(cls=BB)
    b.hello()
