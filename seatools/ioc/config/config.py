import re
from pathlib import Path

from seatools.files import AutoDataFileLoader
from typing import Optional, Dict
from loguru import logger
import os
import types


class _Properties:
    cfg: Optional[Dict] = types.MappingProxyType({})


def load_config(config_dir: str):
    """仅加载`config_dir`中的application.[yml|yaml|json|properties|xml], application-dev.[yml|yaml|json|properties|xml], application-test.[yml|yaml|json|properties|xml], application-pro.[yml|yaml|json|properties|xml]
    :param config_dir: 项目目录地址
    """
    # 当前项目的配置文件
    config_file_path = _find_file_path(config_dir, '^application.(yml|yaml|json|properties|xml)$') or (
            config_dir + os.sep + 'application.yml')
    # 使用 active
    actives = set()

    exist_config_file_path  = os.path.exists(config_file_path)

    _data_file_loader = AutoDataFileLoader()
    # 配置对象_cfg
    _cfg_dict = {}
    if exist_config_file_path:
        _cfg_dict = _merge_config(_cfg_dict, _data_file_loader.load_file(config_file_path,
                                                                         encoding='utf-8'))
        logger.info('加载[{}]配置文件', config_file_path)

    # 优先级 env('ENV') > env('seatools.profiles.active') > application.yml('seatools.profiles.active')
    custom_env = os.getenv('ENV')
    if custom_env:
        actives.add(custom_env)
    else:
        config_actives = os.getenv ('seatools.profiles.active', ((_cfg_dict.get('seatools') or {}).get('profiles') or {}).get('active'))
        if config_actives:
            actives = {*[config_active.strip() for config_active in config_actives.split(',')]}

    for active in actives:
        active_config_file_path = _find_file_path(config_dir, f'^application-{active}.(yml|yaml|json|properties|xml)$')
        if not active_config_file_path:
            continue
        if not os.path.exists(active_config_file_path):
            continue
        _cfg_dict = _merge_config(_cfg_dict, _data_file_loader.load_file(active_config_file_path,
                                                                         encoding='utf-8'))
        logger.info('加载[{}]配置文件', active_config_file_path)

    # 转为不可修改配置信息
    _Properties.cfg = types.MappingProxyType(_cfg_dict)


def _merge_config(cfg1: dict, cfg2: dict) -> dict:
    """ 合并两个配置, 重复的key用cfg2覆盖cfg1 """
    if not cfg2:
        return cfg1
    for key, value in cfg2.items():
        if key in cfg1 and isinstance(cfg1[key], dict) and isinstance(value, dict):
            _merge_config(cfg1[key], value)
        else:
            cfg1[key] = value
    return cfg1


def cfg() -> Optional[Dict]:
    """
    获取配置对象, 需要先调用 load_config, 否则返回空
    Returns:
        配置对象
    """
    return _Properties.cfg


def _find_file_path(config_dir: str, pattern: str) -> Optional[str]:
    """查找符合条件的文件路径, 如果匹配仅返回一个"""
    files = [f for f in Path(config_dir).iterdir() if f.is_file()]
    for file in files:
        if re.match(pattern, file.name):
            return config_dir + os.sep + file.name
    return None
