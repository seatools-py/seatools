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
def new_xxxa_service():  # 涉及依赖可写在方法参数里
    return XXXAService()


@Bean(name='xxxb')
def new_xxxb_service():
    return XXXBService()


"""
xxx/main.py
"""
from seatools.ioc import run, Autowired

def test_ioc():
    # 启动ioc依赖
    run(scan_package_names='tests.test_ioc2', config_dir='./config')
    xxxa = Autowired(
        cls=XXXService)  # 由于XXXService有XXXAService和XXXBService两个子类, 并且均定义了IOC容器实例, 当仅传递类型时, 会自动扫描获取primary=True的Bean返回
    xxxa.do_anything()  # 输出：XXXA
    xxxb = Autowired('xxxb', cls=XXXService)  # 通过名称+类型获取 XXXBService IOC 容器实例
    xxxb.do_anything()  # 输出：XXXB
