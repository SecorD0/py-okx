import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

setup(
    name='py-okx',
    version='1.5.0',
    license='Apache-2.0',
    author='SecorD',
    description='',
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'pretty-utils @ git+https://github.com/SecorD0/pretty-utils@main', 'PySocks', 'python-dotenv', 'requests'
    ],
    keywords=['okx', 'pyokx', 'py-okx', 'okxpy', 'okx-py', 'api', 'okxapi', 'okx-api', 'api-okx'],
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ]
)
