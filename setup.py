#!/usr/bin/env python
"""Setup Tools Script"""
import os
import codecs
from setuptools import setup, find_packages

PACKAGENAME = 'sqre-apikit'
DESCRIPTION = 'LSST Data Management SQuaRE microservice tools'
AUTHOR = 'Adam Thornton'
AUTHOR_EMAIL = 'athornton@lsst.org'
URL = 'https://github.com/lsst-sqre/sqre-apikit'
VERSION = '0.0.10'
LICENSE = 'MIT'


def local_read(filename):
    """Convenience function for includes"""
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return codecs.open(full_filename, 'r', 'utf-8').read()

long_description = local_read('README.md')


setup(
    name=PACKAGENAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='lsst',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'Flask==0.11.1',
        'future==0.16.0'
    ],
    tests_require=['pytest'],
)
