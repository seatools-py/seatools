@echo off

REM 安装依赖
pip install -r requirements.txt

REM 运行文档服务
python serve.py
