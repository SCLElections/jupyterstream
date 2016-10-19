#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='jupyterstream',
    version='1.0.dev',
    description='Streaming the run of a Jupyter notebook',
    author='Cambridge Analytica Data Team',
    install_requires=['numpy', 'pandas', 
                      'matplotlib','nbformat'],
    packages=find_packages(),
    #include_package_data=True
)