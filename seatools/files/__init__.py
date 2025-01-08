from enum import Enum
from typing import Union, Type, Optional, List

from pydantic import BaseModel

from .base import DataFileLoader, DataFileExtractor
from .csv import CsvDataFileLoader, CsvDataFileExtractor
from .yaml import YamlDataFileLoader, YamlDataFileExtractor
from .json import JsonDataFileLoader, JsonDataFileExtractor
from .ini import IniDataFileLoader, IniDataFileExtractor
from .eval import EvalDataFileLoader, EvalDataFileExtractor
from .properties import PropertiesDataFileLoader, PropertiesDataFileExtractor
from .xml import XmlDataFileLoader, XmlDataFileExtractor
from .excel import ExcelDataFileLoader, ExcelDataFileExtractor
from .py import PyDataFileLoader, PyDataFileExtractor

_csv_data_file_loader = CsvDataFileLoader()
_csv_data_file_extractor = CsvDataFileExtractor()
_yaml_data_file_loader = YamlDataFileLoader()
_yaml_data_file_extractor = YamlDataFileExtractor()
_json_data_file_loader = JsonDataFileLoader()
_json_data_file_extractor = JsonDataFileExtractor()
_ini_data_file_loader = IniDataFileLoader()
_ini_data_file_extractor = IniDataFileExtractor()
_properties_data_file_loader = PropertiesDataFileLoader()
_properties_data_file_extractor = PropertiesDataFileExtractor()
_eval_data_file_loader = EvalDataFileLoader()
_eval_data_file_extractor = EvalDataFileExtractor()
_xml_data_file_loader = XmlDataFileLoader()
_xml_data_file_extractor = XmlDataFileExtractor()
_excel_data_file_loader = ExcelDataFileLoader()
_excel_data_file_extractor = ExcelDataFileExtractor()
_py_data_file_loader = PyDataFileLoader()
_py_data_file_extractor = PyDataFileExtractor()


class DataType(Enum):
    """ 数据类型 """
    JSON = (('json',),
            _json_data_file_loader.load, _json_data_file_loader.load_file,
            _json_data_file_extractor.extract, _json_data_file_extractor.extract_file)
    YAML = (('yaml', 'yml'),
            _yaml_data_file_loader.load, _yaml_data_file_loader.load_file,
            _yaml_data_file_extractor.extract, _yaml_data_file_extractor.extract_file)
    INI = (('ini', 'toml', 'cfg'),
           _ini_data_file_loader.load, _ini_data_file_loader.load_file,
           _ini_data_file_extractor.extract, _ini_data_file_extractor.extract_file)
    PROPERTIES = (('properties',),
                  _properties_data_file_loader.load, _properties_data_file_loader.load_file,
                  _properties_data_file_extractor.extract, _properties_data_file_extractor.extract_file)
    CSV = (('csv', ),
           _csv_data_file_loader.load, _csv_data_file_loader.load_file,
           _csv_data_file_extractor.extract, _csv_data_file_extractor.extract_file)
    EVAL = (('eval',),
            _eval_data_file_loader.load, _eval_data_file_loader.load_file,
            _eval_data_file_extractor.extract, _eval_data_file_extractor.extract_file)
    XML = (('xml', 'html'),
           _xml_data_file_loader.load, _xml_data_file_loader.load_file,
           _xml_data_file_extractor.extract, _xml_data_file_extractor.extract_file)
    EXCEL = (('xls', 'xlsx'),
             _excel_data_file_loader.load, _excel_data_file_loader.load_file,
             _excel_data_file_extractor.extract, _excel_data_file_extractor.extract_file)
    PY = (('py', 'pyi', 'pyx'),
          _py_data_file_loader.load, _py_data_file_loader.load_file,
          _py_data_file_extractor.extract, _py_data_file_extractor.extract_file)


def get_file_data_type(file_path: str) -> Optional[DataType]:
    """获取文件的数据类型枚举, 若识别不了则返回None

    Args:
        file_path: 文件路径
    """
    file_type = file_path.split('.')[-1]
    file_data_type = None
    for data_type in DataType:
        if file_type in data_type.value[0]:
            file_data_type = data_type
            break
    return file_data_type


def _parse_data_type(data_type: Union[DataType, str]):
    if isinstance(data_type, DataType):
        return data_type
    if isinstance(data_type, str):
        data_type = data_type.lower()
        for item in DataType:
            if data_type in item.value[0]:
                return item
    raise ValueError('不支持的数据类型: {}'.format(data_type))


class AutoDataFileLoader(DataFileLoader):
    """
    动态检测数据/文件类型加载器
    """

    def load(self,
             config_data: Union[str, bytes],
             modelclass: Union[Type[dict], Type[BaseModel]] = dict,
             data_type: Union[DataType, str, None] = None,
             header=False,
             **kwargs) -> Union[dict, list, BaseModel]:
        """加载配置数据到python或pydantic模型
        Args:
            config_data: 数据字符串
            modelclass: 模型类型
            data_type: 数据类型, None 表示自动解析 (若知道数据类型推荐传入指定数据类型, 防止自动推断类型错误), 传入支持传入DataType枚举以及类型字符串如: json, xml, yaml, yml, properties等DataType支持的解析的类型
            header: 第一行是否为表头, 仅支持CSV传参
        """
        if data_type:
            data_type = self._parse_data_type(data_type)
            return data_type.value[1](config_data,
                                      modelclass=modelclass,
                                      header=header,
                                      use_header_as_key=header)

        for data_type in DataType:
            try:
                return data_type.value[1](config_data,
                                          modelclass=modelclass,
                                          header=header,
                                          use_header_as_key=header)
            except Exception:
                pass
        raise ValueError('无法解析的数据: ' + config_data)

    def load_file(self,
                  file_path: str,
                  encoding: str = 'utf-8',
                  modelclass: Union[Type[dict], Type[BaseModel]] = dict,
                  **kwargs) -> Union[dict, list, BaseModel]:
        """加载文件数据到python对象或pydantic模型

        Args:
            file_path: 文件路径
            encoding: 文件编码类型
            modelclass: 模型类型
        """
        data_type = get_file_data_type(file_path)
        if data_type:
            return data_type.value[2](file_path,
                                      encoding=encoding,
                                      modelclass=modelclass,
                                      **kwargs)

        for data_type in DataType:
            try:
                return data_type.value[2](file_path,
                                          encoding=encoding,
                                          modelclass=modelclass,
                                          **kwargs)
            except Exception:
                pass
        raise ValueError('无法解析的文件: ' + file_path)

    def _parse_data_type(self, data_type: Union[DataType, str]):
        return _parse_data_type(data_type)


DynamicDataFileLoader = AutoDataFileLoader


class DynamicDataFileExtractor(DataFileExtractor):
    """
    动态检测数据特定文件数据类型抽取器
    """

    def extract(self, data: Union[dict, List[dict], BaseModel, List[BaseModel]],
                data_type: Union[DataType, str] = DataType.JSON,
                header=True,
                **kwargs) -> str:
        """数据抽取为特定文件格式的字符串数据

        Args:
            data: 数据
            data_type: 数据类型, 支持DataType类型与字符串类型, 字符串类型传入: json, yaml, yml, csv, properties等DataType中支持的名称, 不支持的名称会抛出ValueError
            header: 第一行是否为表头, 仅支持CSV传参
        """
        data_type = self._parse_data_type(data_type)
        return data_type.value[3](data, header=header, **kwargs)

    def extract_file(self,
                     file_path: str,
                     data: Union[dict, List[dict], BaseModel, List[BaseModel]],
                     encoding: str = 'utf-8',
                     header=True,
                     **kwargs) -> str:
        """数据抽取为特定文件格式的文件字符串并保存至文件

        Args:
            file_path: 文件路径
            data: 数据
            encoding: 文件编码类型
            header: 第一行是否为表头, 仅支持CSV传参
        """
        data_type = get_file_data_type(file_path)
        return data_type.value[4](file_path, data, encoding=encoding, header=header, **kwargs)

    def _parse_data_type(self, data_type: Union[DataType, str]):
        return _parse_data_type(data_type)
