#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
from os.path import dirname, join

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='Chatroom Server',
    version='1.0.0',
    license='BSD 2.0',
    description='A simple Chatroom Server using TCP protocol',
    author='Christos Galanopoulos',
    author_email='christosgalanop@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: BSD License",
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ],
    python_requires='>=3.5',
    install_requires=[
        'pandas', 'openpyxl'
    ],
    project_urls={
        'Source': '',
    },
)
