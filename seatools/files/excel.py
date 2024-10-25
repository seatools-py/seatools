from loguru import logger as log
from typing import Union, List
from pydantic import BaseModel

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from .base import DataFileLoader, DataFileExtractor


class ExcelDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       sheet_name: Union[str, int] = 0,
                                       **kwargs) -> Union[dict, tuple, list]:
        try:
            import pandas
            return pandas.read_excel(config_data, sheet_name=sheet_name).to_dict('records')
        except ImportError as e:
            log.warning('未安装pandas模块, 无法解析excel格式数据')
            raise e

    def _read_normal_file_data(self, file_path: str, encoding: str = 'utf-8') -> Union[str, bytes]:
        with open(file_path, 'rb') as f:
            return f.read()


class ExcelDataFileExtractor(DataFileExtractor):

    def extract(self, data: Union[dict, List[dict], BaseModel, List[BaseModel]],
                **kwargs) -> str:
        raise NotImplementedError('excel不支持仅抽取数据')

    def extract_file(self,
                     file_path: str,
                     data: Union[dict, List[dict], BaseModel, List[BaseModel]],
                     sheet_name: str = 'Sheet1',
                     engine: Literal["openpyxl", "xlsxwriter"] = 'openpyxl',
                     **kwargs) -> str:
        if isinstance(data, (dict, BaseModel)):
            data = [data]
        data = [item.model_dump(mode='json') if isinstance(data, BaseModel) else item for item in data]
        for item in data:
            for k in item:
                item[k] = self._extract_value(item[k])
        try:
            import pandas
            df = pandas.DataFrame(data)
            df.to_excel(file_path, index=False, sheet_name=sheet_name, engine=engine)
            return file_path
        except ImportError as e:
            log.warning('未安装pandas模块, 无法将数据写入为excel文件')
            raise e

