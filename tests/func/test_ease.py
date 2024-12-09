import pytest
import math

from seatools.base import round_
from seatools.func.ease import (
    ease_in_sine, ease_out_sine, ease_in_out_sine,
    ease_in_quad, ease_out_quad, ease_in_out_quad,
    ease_in_cubic, ease_out_cubic, ease_in_out_cubic,
    ease_in_quart, ease_out_quart, ease_in_out_quart,
    ease_in_quint, ease_out_quint, ease_in_out_quint,
    ease_in_expo, ease_out_expo, ease_in_out_expo,
    ease_in_circ, ease_out_circ, ease_in_out_circ,
    ease_in_back, ease_out_back, ease_in_out_back,
    ease_in_elastic, ease_out_elastic, ease_in_out_elastic,
    ease_in_bounce, ease_out_bounce, ease_in_out_bounce
)


# 测试ease_in_sine函数
def test_ease_in_sine():
    assert 0 <= ease_in_sine(0) <= 1
    assert 0 <= ease_in_sine(1) <= 1
    assert ease_in_sine(0.5) == 1 - math.sin(math.pi / 4)


# 测试ease_out_sine函数
def test_ease_out_sine():
    assert 0 <= ease_out_sine(0) <= 1
    assert 0 <= ease_out_sine(1) <= 1
    assert ease_out_sine(0.5) == math.cos(math.pi / 4)


# 测试ease_in_out_sine函数
def test_ease_in_out_sine():
    assert 0 <= ease_in_out_sine(0) <= 1
    assert 0 <= ease_in_out_sine(1) <= 1
    assert round_(ease_in_out_sine(0.5), 1) == 0.5
    assert round_(ease_in_out_sine(0.5), 1) == -math.cos(math.pi) / 2


# 测试ease_in_quad函数
def test_ease_in_quad():
    assert 0 <= ease_in_quad(0) <= 1
    assert 0 <= ease_in_quad(1) <= 1
    assert ease_in_quad(0.5) == 0.5 ** 2


# 测试ease_out_quad函数
def test_ease_out_quad():
    assert 0 <= ease_out_quad(0) <= 1
    assert 0 <= ease_out_quad(1) <= 1
    assert ease_out_quad(0.5) == 1 - (1 - 0.5) ** 2


# 测试ease_in_out_quad函数
def test_ease_in_out_quad():
    assert 0 <= ease_in_out_quad(0) <= 1
    assert 0 <= ease_in_out_quad(1) <= 1
    assert ease_in_out_quad(0.25) == 0.25 ** 2 * 2
    assert ease_in_out_quad(0.75) == 1 - math.pow(-2 * 0.75 + 2, 2) / 2


# 测试ease_in_cubic函数
def test_ease_in_cubic():
    assert 0 <= ease_in_cubic(0) <= 1
    assert 0 <= ease_in_cubic(1) <= 1
    assert ease_in_cubic(0.5) == (0.5) ** 3


# 测试ease_out_cubic函数
def test_ease_out_cubic():
    assert 0 <= ease_out_cubic(0) <= 1
    assert 0 <= ease_out_cubic(1) <= 1
    assert ease_out_cubic(0.5) == 1 - (1 - 0.5) ** 3


# 测试ease_in_out_cubic函数
def test_ease_in_out_cubic():
    assert 0 <= ease_in_out_cubic(0) <= 1
    assert 0 <= ease_in_out_cubic(1) <= 1
    assert ease_in_out_cubic(0.25) == 0.25 ** 3 * 4
    assert ease_in_out_cubic(0.75) == 1 - math.pow(-2 * 0.75 + 2, 3) / 2


# 测试ease_in_quart函数
def test_ease_in_quart():
    assert 0 <= ease_in_quart(0) <= 1
    assert 0 <= ease_in_quart(1) <= 1
    assert ease_in_quart(0.5) == (0.5) ** 4


# 测试ease_out_quart函数
def test_ease_out_quart():
    assert 0 <= ease_out_quart(0) <= 1
    assert 0 <= ease_out_quart(1) <= 1
    assert ease_out_quart(0.5) == 1 - (1 - 0.5) ** 4


# 测试ease_in_out_quart函数
def test_ease_in_out_quart():
    assert 0 <= ease_in_out_quart(0) <= 1
    assert 0 <= ease_in_out_quart(1) <= 1
    assert ease_in_out_quart(0.25) == 0.25 ** 4 * 8
    assert ease_in_out_quart(0.75) == 1 - math.pow(-2 * 0.75 + 2, 4) / 2


# 测试ease_in_quint函数
def test_ease_in_quint():
    assert 0 <= ease_in_quint(0) <= 1
    assert 0 <= ease_in_quint(1) <= 1
    assert ease_in_quint(0.5) == (0.5) ** 5


# 测试ease_out_quint函数
def test_ease_out_quint():
    assert 0 <= ease_out_quint(0) <= 1
    assert 0 <= ease_out_quint(1) <= 1
    assert ease_out_quint(0.5) == 1 - (1 - 0.5) ** 5


# 测试ease_in_out_quint函数
def test_ease_in_out_quint():
    assert 0 <= ease_in_out_quint(0) <= 1
    assert 0 <= ease_in_out_quint(1) <= 1
    assert ease_in_out_quint(0.25) == (0.25) ** 5 * 16
    assert ease_in_out_quint(0.75) == 1 - math.pow(-2 * 0.75 + 2, 5) / 2


# 测试ease_in_expo函数
def test_ease_in_expo():
    assert ease_in_expo(0) == 0
    assert 0 <= ease_in_expo(1) <= 1


# 测试ease_out_expo函数
def test_ease_out_expo():
    assert 0 <= ease_out_expo(0) <= 1
    assert ease_out_expo(1) == 1
    assert ease_out_expo(0.5) == 1 - math.pow(2, -5)


# 测试ease_in_out_expo函数
def test_ease_in_out_expo():
    assert ease_in_out_expo(0) == 0
    assert ease_in_out_expo(1) == 1


# 测试ease_in_circ函数
def test_ease_in_circ():
    assert ease_in_circ(0) == 0
    assert 0 <= ease_in_circ(1) <= 1
    assert ease_in_circ(0.5) == 1 - math.sqrt(1 - 0.5 ** 2)


# 测试ease_out_circ函数
def test_ease_out_circ():
    assert 0 <= ease_out_circ(0) <= 1
    assert ease_out_circ(1) == 1
    assert ease_out_circ(0.5) == 1 - math.sqrt(1 - 0.5 ** 2)


# 测试ease_in_out_circ函数
def test_ease_in_out_circ():
    assert ease_in_out_circ(0) == 0
    assert ease_in_out_circ(1) == 1
    assert ease_in_out_circ(0.25) == (1 - math.sqrt(1 - 0.5 ** 2)) / 2


# 测试ease_in_back函数
def test_ease_in_back():
    assert 0 <= ease_in_back(0) <= 1
    assert 0 <= ease_in_back(1) <= 1


# 测试ease_out_back函数
def test_ease_out_back():
    assert 0 <= ease_out_back(0) <= 1
    assert 0 <= ease_out_back(1) <= 1


# 测试ease_in_out_back函数
def test_ease_in_out_back():
    assert 0 <= ease_in_out_back(0) <= 1
    assert 0 <= ease_in_out_back(1) <= 1


# 测试ease_in_elastic函数
def test_ease_in_elastic():
    assert ease_in_elastic(0) == 0
    assert 0 <= ease_in_elastic(1) <= 1


# 测试ease_out_elastic函数
def test_ease_out_elastic():
    assert 0 <= ease_out_elastic(0) <= 1
    assert ease_out_elastic(1) == 1
    assert ease_out_elastic(0.5) == math.pow(2, -5) * math.sin((5 - 0.75) * (2 * math.pi) / 3) + 1


# 测试ease_in_out_elastic函数
def test_ease_in_out_elastic():
    assert ease_in_out_elastic(0) == 0
    assert ease_in_out_elastic(1) == 1


# 测试ease_in_bounce函数
def test_ease_in_bounce():
    assert 0 <= ease_in_bounce(1) <= 1


# 测试ease_out_bounce函数
def test_ease_out_bounce():
    assert 0 <= ease_out_bounce(0) <= 1


# 测试ease_in_out_bounce函数
def test_ease_in_out_bounce():
    assert ease_in_out_bounce(0) <= 0
    assert ease_in_out_bounce(1) >= 0
