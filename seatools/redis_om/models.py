from typing import Optional, TypeVar
from seatools.models import BaseModel
import redis
from redis_om import HashModel as _HashModel, JsonModel as _JsonModel, EmbeddedJsonModel as _EmbeddedJsonModel, \
    RedisModel, Field, get_redis_connection

Model = TypeVar("Model", bound="RedisModel")


class HashModel(BaseModel, _HashModel):

    def save(
        self: "Model", pipeline: Optional[redis.client.Pipeline] = None
    ) -> "Model":
        self.check()
        db = self._get_db(pipeline)
        document = self.model_dump(mode='json')

        # filter out values which are `None` because they are not valid in a HSET
        document = {k: v for k, v in document.items() if v is not None}
        # TODO: Wrap any Redis response errors in a custom exception?
        db.hset(self.key(), mapping=document)
        return self


class JsonModel(BaseModel, _JsonModel):
    pass


class EmbeddedJsonModel(BaseModel, _EmbeddedJsonModel):
    pass
