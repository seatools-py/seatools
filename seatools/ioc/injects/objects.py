from seatools.ioc.beans.proxy import DelayAutowiredClassBeanProxy, DelayConfigAutowiredClassBeanProxy
from seatools.ioc.constants import required


class Autowired:
    """依赖自动注入"""

    def __new__(_, value: str = None, *, cls=None, required: bool = True):
        """注入对象

        Args:
            value: bean name
            required: 是否必须, 为true找不到注入对象会报错
        """
        return DelayAutowiredClassBeanProxy(name=value, obj=cls, required=required)


class Value:
    """配置自动注入"""
    _cache = {}

    def __new__(_, value: str, *args, cls=None, default_value=required):
        """参数注入

        Args:
            value: 配置名称, 多级使用.分隔, 示例: xxx.xxx
            cls: value读取数据的类型, 如果为None则返回环境变量中的值
            default_value: 默认值, 若不传则表示必须有配置值
        """
        if not value:
            raise ValueError('value配置名称不能为空')
        return DelayConfigAutowiredClassBeanProxy(name=value, obj=cls, default_value=default_value)
