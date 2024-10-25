# 安装依赖
pip install twine setuptools
# 安装
python setup.py sdist bdist_wheel
# 上传
twine upload dist/*
