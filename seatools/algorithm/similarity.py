import math
from typing import Union, List


def cos_similarity(a: Union[float, List[float]], b: Union[float, List[float]], normalized: bool = False) -> float:
    """余弦相似度计算, 支持皮尔逊相关系数

    Args:
        a: 计算的元素或列表
        b: 计算的元素或列表
        normalized: 是否标准化处理, Ture=是, False=否, 标准化处理变为皮尔逊相关系数
    """
    if isinstance(a, float) and isinstance(b, float):
        if a * b == 0:
            return 0
        return a * b / (abs(a) * abs(b))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) == len(b):
            top, down_a, down_b = 0, 0, 0
            normalized_avg_a = (sum(a) / len(a)) if normalized else 0
            normalized_avg_b = (sum(b) / len(b)) if normalized else 0
            for i in range(len(a)):
                top += (a[i] - normalized_avg_a) * (b[i] - normalized_avg_b)
                down_a += (a[i] - normalized_avg_a) ** 2
                down_b += (b[i] - normalized_avg_b) ** 2
            if top == 0 or down_a == 0 or down_b == 0:
                return 0
            return top / (math.sqrt(down_a) * math.sqrt(down_b))
    raise ValueError('格式不匹配无法进行相似度计算')
