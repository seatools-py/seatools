from seatools.env import get_env
from seatools.files import AutoDataFileLoader
from typing import Optional, Dict
from loguru import logger
import os
import types


class _Properties:
    cfg: Optional[Dict] = None


def load_config(config_dir: str):
    """仅加载`config_dir`中的application.yml, application-dev.yml, application-test.yml, application-pro.yml
    :param config_dir: 项目目录地址
    """
    # 当前项目的配置文件
    config_file_path = config_dir + os.sep + f'application.yml'
    # 多环境配置文件
    env_config_file_path = config_dir + os.sep + f'application-{get_env().name}.yml'
    exist_config_file_path, exist_env_config_file_path = os.path.exists(config_file_path), os.path.exists(
        env_config_file_path)
    _data_file_loader = AutoDataFileLoader()
    # 配置对象_cfg
    _cfg_dict = {}
    if exist_config_file_path:
        _cfg_dict = _merge_config(_cfg_dict, _data_file_loader.load_file(config_file_path,
                                                                         encoding='utf-8'))
        logger.info('加载[{}]配置文件', config_file_path)
    if exist_env_config_file_path:
        _cfg_dict = _merge_config(_cfg_dict, _data_file_loader.load_file(env_config_file_path,
                                                                         encoding='utf-8'))
        logger.info('加载[{}]配置文件', env_config_file_path)
    # 转为不可读配置信息
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
