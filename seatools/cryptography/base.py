from typing import Union


def _convert_data(data: Union[str, bytes],
                  encoding='utf-8') -> bytes:
    if isinstance(data, str):
        data = data.encode(encoding=encoding)
    return data
