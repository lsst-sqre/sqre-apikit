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
VERSION = '0.1.3'
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
    long_description_content_type="text/markdown",
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
        'future==0.16.0',
        'requests>=2.13.0,<3.0.0',
        'structlog>=16.1.0',
        # Flask <0.12.4 is incompatible with werkzeug>1.0 but doesn't
        # constrain its version.  The mix produces errors about `is_xhr`.
        'werkzeug<1.0',
    ],
    tests_require=['pytest'],
)
