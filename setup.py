#!/usr/bin/env python3

import sys
from os import path
from setuptools import setup

if not sys.version_info[0] == 3:
    sys.exit("Python 2.x is not supported; Python 3.x is required.")

########################################

version_py = path.join(path.dirname(__file__), '__version__.py')

d = {}
with open(version_py, 'r') as fh:
    exec(fh.read(), d)
    version_pep = d['__version__']

########################################

setup(
    name="motoflash2sh",
    version=version_pep,
    description=("Convert Motorola flashfile.xml to fastboot shell script"),
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author="Daniel Lenski",
    author_email="dlenski@gmail.com",
    license='GPL v3 or later',
    url="https://github.com/dlenski/motoflash2sh",
    py_modules=[ 'motoflash2sh' ],
    entry_points={ 'console_scripts': [ 'motoflash2sh=motoflash2sh:main' ] },
    python_requires=">=3",
)
