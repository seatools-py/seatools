import os
import json
from loguru import logger as log
from abc import ABC
from typing import Union, Type, List, Any
from pydantic import BaseModel


def _read_normal_file_data(file_path: str, encoding: str = 'utf-8') -> str:
    with open(file_path, encoding=encoding) as f:
        config_data = f.read()
    return config_data


class DataFileLoader(ABC):
    """数据/文件加载器, 可将str, bytes类型数据或文件数据加载为python基本数据类型或pydantic模型"""

    def load(self,
             config_data: Union[str, bytes],
             encoding: str = 'utf-8',
             modelclass: Union[Type[dict], Type[BaseModel]] = dict,
             **kwargs) -> Union[dict, list, BaseModel]:
        """解析数据字符串到python dict或pydantic.BaseModel子类实例中

        Args:
            config_data: 数据字符串
            encoding: 数据编码类型, config_data 为 bytes 类型需传
            modelclass: 解析的每个记录的模型类型
        """
        model_data = self._convert_config_data_to_python(
            config_data, encoding=encoding, **kwargs)
        if isinstance(model_data, (tuple, list)):
            for i in range(len(model_data)):
                model_data[i] = self._convert_item_to_model(
                    model_data[i], modelclass=modelclass)
            return model_data
        return self._convert_item_to_model(model_data, modelclass=modelclass)

    def load_file(self,
                  file_path: str,
                  encoding: str = 'utf-8',
                  modelclass: Union[Type[dict], Type[BaseModel]] = dict,
                  **kwargs) -> Union[dict, list, BaseModel]:
        """解析文件数据字符串到python dict或pydantic.BaseModel子类实例中

        Args:
            file_path: 文件路径
            encoding: 文件编码
            modelclass: 解析的每个记录的模型类型
        """
        config_data = _read_normal_file_data(
            file_path=file_path, encoding=encoding)
        return self.load(config_data, encoding=encoding, modelclass=modelclass, **kwargs)

    def _convert_item_to_model(self, item: Union[dict, tuple, list],
                               modelclass: Union[Type[dict], Type[list], Type[tuple], Type[BaseModel]]):
        """将单个元素从dict, tuple, list 转换为指定的 modelclass

        Args:
            item: 单个元素类型
            modelclass: 解析的每个记录的模型类型
        """
        if isinstance(item, (tuple, list)):
            # 数组无法转直接返回
            if modelclass not in (tuple, list):
                log.warning(
                    '数据为tuple或list类型, 无法转为指定modelclass: %s, 直接返回', modelclass)
            return item
        if item and isinstance(item, dict):
            return modelclass(**item)
        return item

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       encoding: str = 'utf-8',
                                       **kwargs) -> Union[dict, tuple, list]:
        """将数据字符串转为python对象

        Args:
            config_data: 数据
        """
        raise NotImplementedError()


class DataFileExtractor(ABC):
    """数据/文件提取器, 可将python基本数据类型或pydantic模型提取为特定文件格式的字符串或文件"""

    def extract(self, data: Union[dict, List[dict], BaseModel, List[BaseModel]],
                **kwargs) -> str:
        """将数据转为指定文件格式的数据字符串

        Args:
            data: 数据
        """
        if isinstance(data, list) and len(data):
            data = [self._normalize_data(item) for item in data]
        else:
            data = self._normalize_data(data)
        return self._convert_data_to_str(data)

    def extract_file(self,
                     file_path: str,
                     data: Union[dict, List[dict], BaseModel, List[BaseModel]],
                     encoding: str = 'utf-8',
                     **kwargs) -> str:
        """将数据转为指定文件格式的字符串并保存到file_path中

        Args:
            file_path: 需要保存的文件路径
            data: 数据
            encoding: 文件的编码格式
        """
        file_data = self.extract(data=data)
        file_path_dir = os.path.dirname(file_path)
        assert os.path.exists(file_path_dir), '目录[{}]不存在, 无法将数据保存到[{}]中'.format(
            file_path_dir, file_path
        )
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(file_data)
        return file_data

    def _normalize_data(self, data: Union[dict, BaseModel]):
        if isinstance(data, dict):
            return data
        return data.model_dump(mode='json')

    def _extract_value(self, v: Any) -> str:
        """抽取值并转为字符串

        Args:
            v: 任意值

        Returns:
            值的字符串映射
        """
        if v is None:
            return ''
        if isinstance(v, BaseModel):
            v = self._normalize_data(v)
        if isinstance(v, (tuple, list, dict)):
            return json.dumps(v, ensure_ascii=False)
        if isinstance(v, bool):
            return str(v).lower()
        return str(v)

    def _convert_data_to_str(self, data: Union[dict, List[dict]]):
        """将python对象转为数据字符串

        Args:
            data: 数据
        """
        raise NotImplementedError()
