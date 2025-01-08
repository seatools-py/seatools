import re
from pathlib import Path

from seatools.files import AutoDataFileLoader
from seatools.utils import dict_utils
from seatools.ioc.utils import value_utils
from typing import Optional, Dict, Union
from loguru import logger
import os
import types


class _Properties:
    cfg: Optional[Dict] = types.MappingProxyType({})
    express_pattern = re.compile(r'\$\{(.*?)\}')


def load_config(config_dir: str):
    """仅加载`config_dir`中的application.[yml|yaml|json|properties|xml], application-dev.[yml|yaml|json|properties|xml], application-test.[yml|yaml|json|properties|xml], application-pro.[yml|yaml|json|properties|xml]
    :param config_dir: 项目目录地址
    """
    # 当前项目的配置文件
    config_file_path = _find_file_path(config_dir, '^application.(yml|yaml|json|properties|xml|py)$') or (
            config_dir + os.sep + 'application.yml')
    # 使用 active
    actives = []

    exist_config_file_path  = os.path.exists(config_file_path)

    _data_file_loader = AutoDataFileLoader()
    # 配置对象_cfg
    _cfg_dict = {}
    if exist_config_file_path:
        _cfg_dict = dict_utils.deep_update(_cfg_dict, _data_file_loader.load_file(config_file_path,
                                                                         encoding='utf-8'))
        logger.info('加载[{}]配置文件', config_file_path)

    # 优先级 env('ENV') > env('seatools.profiles.active') > application.yml('seatools.profiles.active')
    custom_env = os.getenv('ENV')
    if custom_env:
        actives.append(custom_env)
    else:
        config_actives = os.getenv ('seatools.profiles.active', ((_cfg_dict.get('seatools') or {}).get('profiles') or {}).get('active'))
        if config_actives:
            actives = [config_active.strip() for config_active in config_actives.split(',')]

    for active in actives:
        active_config_file_path = _find_file_path(config_dir, f'^application-{active}.(yml|yaml|json|properties|xml|py)$')
        if not active_config_file_path:
            continue
        if not os.path.exists(active_config_file_path):
            continue
        _cfg_dict = dict_utils.deep_update(_cfg_dict, _data_file_loader.load_file(active_config_file_path,
                                                                         encoding='utf-8'))
        logger.info('加载[{}]配置文件', active_config_file_path)

    # 解析配置中的变量
    _parse_cfg_dict(_cfg_dict, _cfg_dict)

    # 转为不可修改配置信息
    _Properties.cfg = types.MappingProxyType(_cfg_dict)


def _parse_cfg_dict(cfg_dict: dict, scan_cfg_dict: dict):
    """解析配置中的变量."""
    for k, v in scan_cfg_dict.items():
        if isinstance(v, dict):
            _parse_cfg_dict(cfg_dict, v)
            continue
        if isinstance(v, (list, tuple)):
            _parse_cfg_list(cfg_dict, v)
            continue
        scan_cfg_dict[k] = _parse_cfg_dict_value(cfg_dict, v)


def _parse_cfg_list(cfg_dict: dict, scan_cfg_list: Union[list, tuple]):
    for index in range(len(scan_cfg_list)):
        scan = scan_cfg_list[index]
        if isinstance(scan, dict):
            _parse_cfg_dict(cfg_dict, scan)
            continue
        if isinstance(scan, (list, tuple)):
            _parse_cfg_list(cfg_dict, scan)
            continue
        scan_cfg_list[index] = _parse_cfg_dict_value(cfg_dict, scan)


def _parse_cfg_dict_value(cfg_dict: dict, value):
    if not isinstance(value, str):
        return value
    expresses = list(set(_Properties.express_pattern.findall(value)))
    if not expresses:
        return value
    if len(expresses) == 1 and '${' + expresses[0] + '}' == value:
        return _parse_cfg_dict_value(cfg_dict, _parse_cfg_express_value(cfg_dict, expresses[0]))
    else:
        new_value = value
        for exp in expresses:
            new_value = new_value.replace('${' + exp + '}', f'{_parse_cfg_express_value(cfg_dict, exp)}')
        return new_value


def _parse_cfg_express_value(cfg_dict: dict, express):
    v = value_utils.parse_express_value(cfg_dict, express)
    if v is None:
        v = '${' + express + '}'
    return _parse_cfg_dict_value(cfg_dict, v)


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
