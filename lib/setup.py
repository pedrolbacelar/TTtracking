import os
import sys
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tttracking',
    packages=find_packages(),
    version= '0.0.1.2',
    description= 'TTtracking MVP',
    author='Pedro Bacelar',
    license='MIT',
    long_description=long_description
)