import os
from seatools.env import get_env


def test_dev_env():
    os.environ['ENV'] = 'dev'
    print(get_env().is_dev())
    print(get_env().is_test())
    print(get_env().is_pro())
    print(get_env())


def test_test_env():
    os.environ['ENV'] = 'test'
    print(get_env().is_dev())
    print(get_env().is_test())
    print(get_env().is_pro())
    print(get_env())


def test_pro_env():
    os.environ['ENV'] = 'pro'
    print(get_env().is_dev())
    print(get_env().is_test())
    print(get_env().is_pro())
    print(get_env())


def test_other_env():
    os.environ['ENV'] = 'xxx'
    print(get_env().is_dev())
    print(get_env().is_test())
    print(get_env().is_pro())
    print(get_env())
