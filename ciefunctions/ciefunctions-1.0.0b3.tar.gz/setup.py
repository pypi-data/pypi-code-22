from setuptools import setup

setup(
    name="ciefunctions",
    version="1.0.0b3",
    packages=['tc1_97', 'web'],
    scripts=['ciefunctions.py'],
    include_package_data=True,
    package_data={'tc1_97': ['data/*', '*.css'],
                  'web': ['static/*']},
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'pyqt5'],
    author="Jan Henrik Wold and Ivar Farup",
    author_email="ivar.farup@ntnu.no",
    description="Desktop and web apps for computing the CIE Functions",
    license="GPL3.0",
    url="https://github.com/ifarup/ciefunctions"
)
