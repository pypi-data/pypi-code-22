from setuptools import setup

setup(name='direqt',
      version='0.1.2',
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 2'
      ],
      description='Client library for Direqt Ads API',
      url='https://github.com/direqt/direqt-sdk-python',
      author='Myk Willis',
      author_email='myk@direqt.io',
      license='Apache License 2.0',
      packages=['direqt'],
      install_requires=[
            'google_auth',
            'requests'
      ],
      platforms='any',
      zip_safe=False)
