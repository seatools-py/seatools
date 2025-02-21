文件处理工具
============

Seatools 提供了丰富的文件格式处理工具。

数据文件加载器
--------------

.. code-block:: python

   from seatools.files import DynamicDataFileLoader

   loader = DynamicDataFileLoader()

   # 加载 YAML
   data = loader.load_file('config.yml')

   # 加载 JSON
   data = loader.load_file('data.json')

   # 加载 CSV
   data = loader.load_file('data.csv')

数据文件导出器
--------------

.. code-block:: python

   from seatools.files import DynamicDataFileExtractor

   extractor = DynamicDataFileExtractor()

   # 导出为 JSON
   extractor.extract_file('output.json', data)

   # 导出为 YAML
   extractor.extract_file('output.yml', data)
