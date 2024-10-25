from seatools.models import BaseModel, R, PageR, PageModel
from loguru import logger
from pydantic import BaseModel as PydanticBaseModel
import datetime


def test_models():
    class AModel(BaseModel):
        a: int
        b: datetime.datetime
        c: datetime.date
        d: datetime.time

    a = AModel(a=1, b='2023-12-31 00:23:21', c='2023-12-31', d='00:23:31')
    print(a.model_dump_json())


def test_r_models():
    print(PageR.ok(data=PageModel()))
    print(R.ok('hello'))


def test_model_to_str():
    class Old(PydanticBaseModel):
        a: str

    class New(BaseModel):
        a: str

    try:
        o = Old(a=1)
        logger.info(o)
    except Exception as e:
        logger.error('pydantic model 异常')

    try:
        n = New(a=True)
        logger.info(n)
    except Exception as e:
        logger.error('自定义 model 异常')
