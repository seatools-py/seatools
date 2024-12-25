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

    def hello_error(self):
        raise RuntimeError


@Aspect
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


def test_ioc_aop_success():
    start()
    a = Autowired(cls=A)
    a.hello("lalala")


def test_ioc_aop_exception():
    start()
    a = Autowired(cls=A)
    with pytest.raises(RuntimeError):
        a.hello_error()

