# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fr:
    required = fr.read().splitlines()

setup(
    name='code_syntax_analyser',
    version='0.0.1',
    packages=['code_syntax_analyser'],
    url='https://github.com/ndrwpvlv/code_syntax_analyser',
    license='',
    author='Andrei S. Pavlov',
    author_email='ndrw.pvlv@gmail.com',
    description='Calculation unique verbs in function names',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
)
