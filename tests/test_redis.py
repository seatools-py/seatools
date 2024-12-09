import json
from typing import List
from seatools.redis_om import HashModel, get_redis_connection, Field


class QuoteModel(HashModel):
    text: str = Field(index=True, full_text_search=True)
    author: str = Field(index=True)
    tags: str

    class Meta:
        database = get_redis_connection(url='redis://:123456@localhost:6379/0')

def test_redis_add():
    qm = QuoteModel(text='aaa', author='bbb', tags=json.dumps(['ccc']))
    qm.save()

