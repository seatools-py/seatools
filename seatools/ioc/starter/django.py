import os
from seatools.ioc import Bean
from seatools.ioc.config import cfg
from loguru import logger


@Bean
def init_django():
    if 'package_name' not in cfg():
        logger.warning('配置不存在[package_name]属性, 无法自动初始化数django')
        return
    package_name = cfg()['package_name']
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{package_name}.django.settings')
    import django
    django.setup()
