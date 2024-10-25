from loguru import logger


def setup(file_name,
          rotation="1 days",
          retention="30 days",
          serialize=True,
          backtrace=True,
          diagnose=False,
          filter=lambda record: True,
          level='INFO'):
    """初始化安装loguru日志配置

    使用方式:
        from loguru import logger

        logger.info('info message')
        logger.error('error message')

    Args:
        file_name: 文件名称
        rotation: 日志滚动周期, 允许值示例如下:
            logger.add("file_1.log", rotation="500 MB")    # Automatically rotate too big file
            logger.add("file_2.log", rotation="12:00")     # New file is created each day at noon
            logger.add("file_3.log", rotation="1 week")    # Once the file is too old, it's rotated
            logger.add("file_X.log", retention="10 days")  # Cleanup after some time
            logger.add("file_Y.log", compression="zip")    # Save some loved space
        retention: 日志文件保留周期, 默认30天
        serialize: 是否将写入文件的数据序列化为json, 默认True. 推荐: True
        backtrace: 是否默认在异常时自动打印堆栈信息, 默认True. 推荐: True
        diagnose: 是否开启代码异常诊断, 可层层递进追踪异常链路, 生产环境建议关闭, 开发环境建议开启, 默认False
        filter: 日志文件的过滤条件, 符合条件的日志记录将写入该文件
        level: 日志级别, 只有超过该级别的日志会记入文件, 支持以下日志级别
            TRACE: 最低级别，用于追踪程序的详细执行流程，通常用于诊断问题
            DEBUG: 用于调试目的的详细信息，例如变量值或者函数调用
            INFO: 提供程序执行中的一般信息，用于表示程序正常运行
            SUCCESS: 表示成功的操作
            WARNING: 表示潜在的问题或者不符合预期的情况，但程序仍能继续执行
            ERROR: 表示错误，但程序仍然可以继续执行
            CRITICAL: 表示严重错误，可能导致程序无法继续执行
    """
    # 添加文件配置
    logger.add(file_name,
               format="{message}",
               backtrace=backtrace,
               diagnose=diagnose,
               serialize=serialize,
               rotation=rotation,
               retention=retention,
               filter=filter,
               level=level)


class PrefixLogger:
    """前缀日志工具, 所有日志内容都将带上[prefix]前缀"""

    def __init__(self, prefix='', _logger=None):
        self._prefix = prefix
        if _logger:
            self._logger = _logger
        else:
            self._logger = logger

    def trace(self, __message, *args, **kwargs):
        return self.log("TRACE", __message, *args, **kwargs)

    def debug(self, __message, *args, **kwargs):
        return self.log("DEBUG", __message, *args, **kwargs)

    def info(self, __message, *args, **kwargs):
        return self.log("INFO", __message, *args, **kwargs)

    def warning(self, __message, *args, **kwargs):
        return self.log("WARNING", __message, *args, **kwargs)

    def error(self, __message, *args, **kwargs):
        return self.log("ERROR", __message, *args, **kwargs)

    def success(self, __message, *args, **kwargs):
        return self.log("SUCCESS", __message, *args, **kwargs)

    def critical(self, __message, *args, **kwargs):
        return self.log("CRITICAL", __message, *args, **kwargs)

    def exception(self, __message, *args, **kwargs):
        if self._prefix:
            return self._logger.exception(f"[{self._prefix}]{__message}", *args, **kwargs)
        return self._logger.exception(__message, *args, **kwargs)

    def log(self, __level, __message, *args, **kwargs):
        if self._prefix:
            return self._logger.log(__level, f"[{self._prefix}]{__message}", *args, **kwargs)
        return self._logger.log(__level, __message, *args, **kwargs)
