# 通用基础实现

__round_mask = 0.00001


def round_(number, decimal: int = 0) -> float:
    """四舍五入, 解决内置round奇进偶舍问题

    Args:
        number: 数值
        decimal: 小数位数

    Returns:
        四舍五入保留的值
    """
    percent = 10**decimal
    number *= percent
    number = round(number + __round_mask / percent)
    # 防止整数转为浮点数
    if decimal > 0:
        number /= percent
    return number
