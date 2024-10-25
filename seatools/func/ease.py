import math


def ease_in_sine(x: float) -> float:
    """缓动函数easeInSine

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 1 - math.cos((x * math.pi) / 2)


def ease_out_sine(x: float) -> float:
    """缓动函数easeOutSine

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return math.sin((x * math.pi) / 2)


def ease_in_out_sine(x: float) -> float:
    """缓动函数easeInOutSine

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return -(math.cos(math.pi * x) - 1) / 2


def ease_in_quad(x: float) -> float:
    """缓动函数easeInQuad

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return x * x


def ease_out_quad(x: float) -> float:
    """缓动函数easeOutQuad

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 1 - (1 - x) * (1 - x)


def ease_in_out_quad(x: float) -> float:
    """缓动函数easeInOutQuad

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 2 * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 2) / 2


def ease_in_cubic(x: float) -> float:
    """缓动函数easeInCubic

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return math.pow(x, 3)


def ease_out_cubic(x: float) -> float:
    """缓动函数easeOutCubic

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 1 - math.pow(1 - x, 3)


def ease_in_out_cubic(x: float) -> float:
    """缓动函数easeInOutCubic

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 4 * x * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 3) / 2


def ease_in_quart(x: float) -> float:
    """缓动函数easeInQuart

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return math.pow(x, 4)


def ease_out_quart(x: float) -> float:
    """缓动函数easeOutQuart

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 1 - math.pow(1 - x, 4)


def ease_in_out_quart(x: float) -> float:
    """缓动函数easeInOutQuart

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 8 * x * x * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 4) / 2


def ease_in_quint(x: float) -> float:
    """缓动函数easeInQuint

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return math.pow(x, 5)


def ease_out_quint(x: float) -> float:
    """缓动函数easeOutQuint

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 1 - math.pow(1 - x, 5)


def ease_in_out_quint(x: float) -> float:
    """缓动函数easeInOutQuint

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 16 * x * x * x * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 5) / 2


def ease_in_expo(x: float) -> float:
    """缓动函数easeInExpo

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 0 if x == 0 else math.pow(2, 10 * x - 10)


def ease_out_expo(x: float) -> float:
    """缓动函数easeOutExpo

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 1 if x == 1 else 1 - math.pow(2, -10 * x)


def ease_in_out_expo(x: float) -> float:
    """缓动函数easeInOutExpo

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    if x == 0:
        return 0
    if x == 1:
        return 1
    return math.pow(2, 20 * x - 10) / 2 if x < 0.5 else (2 - math.pow(2, -20 * x + 10)) / 2


def ease_in_circ(x: float) -> float:
    """缓动函数easeInCirc

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 1 - math.sqrt(1 - math.pow(x, 2))


def ease_out_circ(x: float) -> float:
    """缓动函数easeOutCirc

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 1 - math.sqrt(1 - math.pow(x, 2))


def ease_in_out_circ(x: float) -> float:
    """缓动函数easeInOutCirc

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2 if x < 0.5 else (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2


def ease_in_back(x: float) -> float:
    """缓动函数easeInBack

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * pow(x, 3) - c1 * x * x


def ease_out_back(x: float) -> float:
    """缓动函数easeOutBack

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    c1 = 1.70158
    c3 = c1 + 1

    return 1 + c3 * math.pow(x - 1, 3) + c1 * math.pow(x - 1, 2)


def ease_in_out_back(x: float) -> float:
    """缓动函数easeInOutBack

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    c1 = 1.70158
    c2 = c1 * 1.525

    return (math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2 if x < 0.5 else (math.pow(2 * x - 2, 2) * (
            (c2 + 1) * (x * 2 - 2) + c2) + 2) / 2


def ease_in_elastic(x: float) -> float:
    """缓动函数easeInElastic

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    c4 = (2 * math.pi) / 3
    if x == 0:
        return 0
    if x == 1:
        return 1
    return -math.pow(2, 10 * x - 10) * math.sin((x * 10 - 10.75) * c4)


def ease_out_elastic(x: float) -> float:
    """缓动函数easeOutElastic

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    c4 = (2 * math.pi) / 3
    if x == 0:
        return 0
    if x == 1:
        return 1
    return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1


def ease_in_out_elastic(x: float) -> float:
    """缓动函数easeInOutElastic

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    c5 = c5 = (2 * math.pi) / 4.5
    if x == 0:
        return 0
    if x == 1:
        return 1
    return -(math.pow(2, 20 * x - 10) * math.sin((20 * x - 11.125) * c5)) / 2 if x < 0.5 else (
        (math.pow(2, -20 * x + 10) * math.sin((20 * x - 11.125) * c5)) / 2 + 1
    )


def ease_in_bounce(x: float) -> float:
    """缓动函数easeInBounce

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return 1 - ease_out_bounce(1 - x)


def ease_out_bounce(x: float) -> float:
    """缓动函数easeOutBounce

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    n1 = 7.5625
    d1 = 2.75

    if x < 1 / d1:
        return n1 * x * x
    if x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    if x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    x -= 2.625
    return n1 * x * x + 0.984375


def ease_in_out_bounce(x: float) -> float:
    """缓动函数easeInOutBounce

    Args:
        x: 横轴值, 范围 [0, 1]

    Returns:
        函数纵轴值, 范围 [0, 1]
    """
    return (1 - ease_out_bounce(1 - 2 * x)) / 2 if x < 0.5 else (1 + ease_out_bounce(2 * x - 1)) / 2
