from loguru import logger
from seatools.logger import setup


def setup_loguru(file_name,
                 rotation="1 days",
                 serialize=True,
                 backtrace=True,
                 diagnose=False,
                 retention="3 days",
                 level='INFO',
                 service_name='unknown',
                 label=''):
    """设置loguru日志记录.

    Args:
        file_name: 日志文件路径及名称
        rotation:
        serialize: 是否序列化, 仅为True时生效
        backtrace:
        diagnose:
        retention:
        level: 日志级别
        service_name: 服务名称, 业务参数
        label: 标签, 业务参数
    """
    logger.configure(extra={'service_name': service_name, 'label': label})
    setup(file_name,
          rotation=rotation,
          serialize=serialize,
          backtrace=backtrace,
          diagnose=diagnose,
          retention=retention,
          level=level)
