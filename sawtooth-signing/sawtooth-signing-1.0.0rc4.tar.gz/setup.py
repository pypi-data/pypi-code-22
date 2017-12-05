# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import os
import subprocess

# from distutils.core import setup, Extension, find_packages
from setuptools import setup, Extension, find_packages



setup(
    name='sawtooth-signing',
    version='1.0.0rc4',
    description='Sawtooth Signing Library',
    author='Hyperledger Sawtooth',
    url='https://github.com/hyperledger/sawtooth-core',
    packages=find_packages(),
    install_requires=[
        "bitcoin",
        "secp256k1",
    ],
    data_files=[],
    entry_points={})
