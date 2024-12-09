import pytest

from seatools.algorithm.similarity import cos_similarity
from loguru import logger


def test_cos_similarity():
    a = [0, 0, 0, 1, 1, 0, 1, 0, 1]
    b = [0, 1, 0, 0, 0, 0, 0, 0, 0]
    c = [0, 0, 1, 0, 0, 0, 0, 0, 0]
    d = [1, 1, 1, 1, 1, 1, 1, 0, 1]
    logger.success(cos_similarity(2.3, 4.5))
    logger.success(cos_similarity(0, 4.5))
    logger.success(cos_similarity([0, 0], [0, 0]))
    logger.success(cos_similarity(a, d))
    logger.success(cos_similarity(b, d))
    logger.success(cos_similarity(c, d))
    with pytest.raises(ValueError):
        logger.error(cos_similarity([0, 1], [0, 0, 0]))

