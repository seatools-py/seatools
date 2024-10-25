from seatools.algorithm.similarity import cos_similarity
from loguru import logger


def test_cos_similarity():
    a = [0, 0, 0, 1, 1, 0, 1, 0, 1]
    b = [0, 1, 0, 0, 0, 0, 0, 0, 0]
    c = [0, 0, 1, 0, 0, 0, 0, 0, 0]
    d = [1, 1, 1, 1, 1, 1, 1, 0, 1]
    logger.success('')
    logger.success(cos_similarity(a, d))
    logger.success(cos_similarity(b, d))
    logger.success(cos_similarity(c, d))

