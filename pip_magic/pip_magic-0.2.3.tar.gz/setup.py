#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['pip_magic']

package_data = \
{'': ['*']}

setup(name='pip_magic',
      version='0.2.3',
      description='import this in ipython and use pip magically without ! and correct version !',
      author='Matthias Bussonnier',
      author_email='bussonniermatthias@gmail.com',
      url='https://github.com/Carreau/pip_magic',
      packages=packages,
      package_data=package_data,
     )
