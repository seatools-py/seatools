import json
from typing import Optional

import pytest

from seatools.models import BaseModel
from seatools.files import AutoDataFileLoader, DataType


class TestBModel(BaseModel):
    c: Optional[int] = None
    d: Optional[str] = None


class TestModel(BaseModel):
    a: Optional[int] = None
    b: Optional[TestBModel] = None


def test_file():
    adfl = AutoDataFileLoader()
    # yaml 测试
    print(adfl.load("""
    a: 1
    b:
      c: 2
      d: sadas
    """))
    print(adfl.load("""
        a: 1
        b:
          c: 2
          d: sadas
        """, TestModel))
    print(adfl.load(str({'a': 1, 'b': {'c': 2, 'd': 'sadas'}})))
    print(adfl.load(str({'a': 1, 'b': {'c': 2, 'd': 'sadas'}}), TestModel))
    print(adfl.load(json.dumps({'a': 1, 'b': {'c': 2, 'd': 'sadas'}})))
    print(adfl.load(json.dumps(
        {'a': 1, 'b': {'c': 2, 'd': 'sadas'}}), TestModel))
    print(adfl.load("""
        [b]
        c = 2
        d = sadas
        """))
    print(adfl.load("""
    [b]
    c = 2
    d = sadas
    """, TestModel))

    print(adfl.load("""a,c,d
1,2,3
4,5,6
7,8,9""", header=True))
    print(adfl.load("""a,c,d
1,2,3
4,5,6
7,8,9""", modelclass=TestModel, header=True, data_type=DataType.CSV))
    print(adfl.load("""
b.c=123
b.d=s3434
"""))
    print(adfl.load("""
    b.c=123
    b.d=s3434
    """, modelclass=TestModel))


def test_file_loads(tmp_path):
    adfl = AutoDataFileLoader()
    tmp_file = tmp_path / 'tmp_file.json'
    with open(tmp_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'a': 1, 'b': {'c': 2, 'd': 'sadas'}}))
    adfl.load_file(file_path=tmp_file.as_posix())
