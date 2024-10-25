from loguru import logger as log
from typing import Union, List

from .base import DataFileLoader, DataFileExtractor
import xml.etree.ElementTree as ET


class XmlDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       encoding: str = 'utf-8',
                                       **kwargs) -> Union[dict, tuple, list]:
        try:
            import xmltodict
            return xmltodict.parse(config_data)
        except ImportError as e:
            log.warning('未安装xmltodict模块, 无法解析xml格式数据')
            raise e


class XmlDataFileExtractor(DataFileExtractor):

    def _convert_data_to_str(self, data: Union[dict, List[dict]],
                             encoding='utf-8', **kwargs):
        def dict_to_xml(tag, d):
            """将字典转换为XML元素"""
            elem = ET.Element(tag)
            for key, val in d.items():
                if isinstance(val, dict):
                    # 如果值是字典，递归创建子元素
                    child = dict_to_xml(key, val)
                elif isinstance(val, list):
                    # 如果值是列表，遍历列表并为每个元素创建子元素
                    for item in val:
                        if isinstance(item, dict):
                            child = dict_to_xml(key, item)
                        else:
                            child = ET.Element(key)
                            child.text = self._extract_value(item)
                        elem.append(child)
                    continue
                else:
                    # 如果值不是字典或列表，创建文本元素
                    child = ET.Element(key)
                    child.text = self._extract_value(val)
                elem.append(child)
            return elem

        def dict_to_xml_string(data_dict):
            """将整个字典转换为XML字符串"""
            # 创建字典中所有顶级键的元素
            elements = []
            for key, value in data_dict.items():
                child = dict_to_xml(key, value)
                elements.append(child)
            return '\n'.join([ET.tostring(element, encoding=encoding).decode(encoding) for element in elements])
        if isinstance(data, dict):
            data = [data]
        ans = ''
        for item in data:
            ans += '{}\n'.format(dict_to_xml_string(item))
        return ans

