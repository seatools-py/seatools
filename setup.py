#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = []

with open('requirements.txt', encoding='utf-8') as f:
    for require in f.readlines():
        require = require.strip()
        if require:
            requirements.append(require)

test_requirements = ['pytest>=6.2.4', ]

setup(
    author="dragons96",
    author_email='521274311@qq.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
    ],
    description="python集成工具包",
    install_requires=requirements,
    extras_require={
        'mysql': ['pymysql>=1.1.0'],
        'orm': ['sqlalchemy>=2.0.27'],
        'impala': ['impyla>=0.19.0'],
        'clickhouse': ['clickhouse-driver>=0.2.7'],
        'orm_clickhouse': ['sqlalchemy>=2.0.27', 'clickhouse-sqlalchemy'],
        'hive': ['pyhive', 'thrift', 'thrift-sasl'],
        'fastapi': ['fastapi>=0.110.0', 'uvicorn[standard]>=0.29.0'],
        'aes': ['pycryptodome>=3.20.0'],
        'all': ['pymysql>=1.1.0', 'sqlalchemy>=2.0.27', 'impyla>=0.19.0', 'clickhouse-driver>=0.2.7',
                'fastapi>=0.110.0', 'uvicorn[standard]>=0.29.0', 'pycryptodome>=3.20.0', 'pyhive', 'thrift',
                'thrift-sasl', 'pycryptodome>=3.20.0'],
    },
    license="MIT license",
    long_description='',
    include_package_data=True,
    keywords='seatools',
    name='seatools',
    packages=find_packages(include=['seatools', 'seatools.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitee.com/dragons96/seatools',
    version='1.0.37',
    zip_safe=False,
)
