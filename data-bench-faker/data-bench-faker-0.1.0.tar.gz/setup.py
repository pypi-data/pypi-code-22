#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup


with Path(__file__).absolute().parent.joinpath('README.rst') as f:
    README = f.read_text()

def get_version(filename='Makefile', default_version='0.0.0'):
    '''
    '''
    with Path(__file__).absolute().parent.joinpath(filename) as f:
        for line in f.read_text().split('\n'):
            k,sep,v = line.partition('=')
            if k == 'VERSION':
                return v
    return default_version
        

# this module can be zip-safe if the zipimporter implements iter_modules or if
# pkgutil.iter_importer_modules has registered a dispatch for the zipimporter.
try:
    import pkgutil
    import zipimport
    zip_safe = hasattr(zipimport.zipimporter, "iter_modules") or \
        zipimport.zipimporter in pkgutil.iter_importer_modules.registry.keys()
except (ImportError, AttributeError):
    zip_safe = False

setup(
    name='data-bench-faker',
    version=get_version(),
    description="Data Bench Provider for the Faker Python package.",
    long_description=README,
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License'
    ],
    keywords='faker databench test data',
    author="Erik O\'Shaughnessy",
    author_email='erik.oshaughnessy@intel.com',
    url='https://github.com/ErikOShaughnessy/data-bench-faker',
    license='Apache License, Version 2.0',
    package_dir={'data_bench_faker': 'src/data_bench'},
    packages=['data_bench_faker'],
    platforms=['any'],
    test_suite='pytest',
    zip_safe=zip_safe,
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-flakes',
        'pytest-pep8',
    ],
    install_requires=[
        'faker',
    ],
)
