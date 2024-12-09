from seatools import base


def test_base():
    assert round(3.5) == 4
    assert round(4.5) == 4
    assert base.round_(3.5) == 4
    assert base.round_(4.5) == 5
    assert base.round_(3.55, 1) == 3.6
    assert base.round_(4.55, 1) == 4.6
