#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().split('\n')

with open('requirements-dev.txt') as req_file:
    requirements_dev = req_file.read().split('\n')

with open('VERSION') as fp:
    version = fp.read().strip()

setup(
    name='portia',
    version=version,
    description="Portia",
    long_description=readme,
    author="Praekelt Foundation",
    author_email='dev@praekeltfoundation.org',
    url='https://github.com/praekelt/portia',
    packages=[
        'portia',
    ],
    package_dir={'portia':
                 'portia'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='portia',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': ['portia = portia.cli:main'],
    },
)
