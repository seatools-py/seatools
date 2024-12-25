from typing import Any

import pytest

from seatools.ioc import run, Autowired, Bean, Aspect, AbstractAspect
from seatools.ioc.aop.point import JoinPoint


def start():
    # 启动ioc依赖
    run(scan_package_names='tests.test_ioc_aop', config_dir='./config',
        enable_aspect=True)


@Bean
class A:

    def hello(self, name):
        print(f"hello A {name}")

    def hello_return(self, name):
        return f"hello {name}"

    def hello_error(self):
        raise RuntimeError

    def _hello_protected(self, name):
        print(f"hello A {name}")


@Aspect(order=100)
class AAop(AbstractAspect):

    pointcut = "execution(tests.test_ioc_aop.A.*)"

    def before(self, point: JoinPoint, **kwargs) -> None:
        print('A before')

    def after(self, point: JoinPoint, **kwargs) -> None:
        print('A after')

    def around(self, point: JoinPoint, **kwargs) -> Any:
        print("A around before")
        v = super().around(point, **kwargs)
        print("A around after")
        return v

    def after_returning(self, point: JoinPoint, return_value: Any, **kwargs) -> None:
        print('A after_returning')

    def after_exception(self, point: JoinPoint, ex: Exception, **kwargs) -> None:
        print('A after_exception')


class A2Aop(AbstractAspect):
    pointcut = "execution(tests.test_ioc_aop.A.*)"

    def before(self, point: JoinPoint, **kwargs) -> None:
        print('A2 before')

    def after(self, point: JoinPoint, **kwargs) -> None:
        print('A2 after')

    def around(self, point: JoinPoint, **kwargs) -> Any:
        print("A2 around before")
        v = super().around(point, **kwargs)
        print("A2 around after")
        return v

    def after_returning(self, point: JoinPoint, return_value: Any, **kwargs) -> None:
        print('A2 after_returning')

    def after_exception(self, point: JoinPoint, ex: Exception, **kwargs) -> None:
        print('A2 after_exception')


@Aspect
def a2_aop():
    return A2Aop()


def test_ioc_aop_success():
    start()
    a = Autowired(cls=A)
    a.hello("lala")
    # a._hello_protected("lalala")


def test_ioc_aop_return():
    start()
    a = Autowired(cls=A)
    print(a.hello_return("lalala"))


def test_ioc_aop_exception():
    start()
    a = Autowired(cls=A)
    with pytest.raises(RuntimeError):
        a.hello_error()

