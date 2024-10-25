import os
from enum import Enum
from loguru import logger as log


class EnvEnum(Enum):
    # 开发环境
    dev = 'development'
    # 测试环境
    test = 'test'
    # 生产环境
    pro = 'production'

    def is_dev(self):
        if self.value == 'development':
            return True
        return False

    def is_test(self):
        if self.value == 'test':
            return True
        return False

    def is_pro(self):
        if self.value == 'production':
            return True
        return False


_env = None


def get_env() -> EnvEnum:
    """获取系统当前环境, 仅支持EnvEnum定义的环境名称

    Returns:
        EnvEnum 环境枚举对象
    """
    global _env
    if _env:
        return _env
    os_env = os.getenv('ENV', 'dev').lower()
    for env in EnvEnum:
        if env.name == os_env:
            _env = env
            break
    if not _env:
        _env = EnvEnum.dev
        log.warning('未找到设置的系统环境类型[{}], 当前使用默认环境类型[{}]'.format(os_env, _env.value))
    log.info('当前项目环境: [{}]'.format(_env.name))
    return _env
