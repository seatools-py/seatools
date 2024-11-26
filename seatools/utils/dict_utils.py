

def deep_update(d1: dict, d2: dict) -> dict:
    """深度合并两个配置, 仅覆盖最小层级, 重复的key用cfg2覆盖cfg1.

    注意: 该方法会覆盖d1元数据, 不会新生成字典
    """
    if not d2:
        return d1
    for key, value in d2.items():
        if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
            deep_update(d1[key], value)
        else:
            d1[key] = value
    return d1

