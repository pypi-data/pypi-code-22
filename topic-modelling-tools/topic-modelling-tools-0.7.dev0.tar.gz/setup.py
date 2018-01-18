import sys
from setuptools import setup
from setuptools.extension import Extension

### unit tests for this package
import topicmodel_tests

### set include dirs for numpy

try:
    import numpy
except ImportError:
    numpy_already_installed = False
    from distutils.sysconfig import get_python_lib
    include_numpy_dir = get_python_lib()+"/numpy/core/include"
else:
    numpy_already_installed = True 
    include_numpy_dir = numpy.get_include()   



###  Cython - rebuild the .c from the .pyx file if there, or if not, just use the .c

try:
    from Cython.Distutils import build_ext
##    from Cython.Build import cythonize
except ImportError:
    use_cython = False
else:
    use_cython = True


cmdclass = { }
ext_modules = [ ]

if use_cython:
    ext_modules += [
        Extension("topicmodels.samplers.samplers_lda",
                  ["topicmodels/samplers/samplers_lda.pyx"],
                  include_dirs=[
                      include_numpy_dir,
                  ],
        )
    ]
    cmdclass.update({ 'build_ext': build_ext })
else:
    ext_modules += [
        Extension("topicmodels.samplers.samplers_lda",
                  ["topicmodels/samplers/samplers_lda.c"],
                  include_dirs=[
                      include_numpy_dir,
                  ],                  
        )
    ]

setup(name = "topic-modelling-tools",
      version="0.7dev",
      author="Stephen Hansen",
      url="https://github.com/alan-turing-institute/topic-modelling-tools",
      author_email="stephen.hansen@economics.ox.ac.uk",
      ext_modules=ext_modules,
      packages=['topicmodels', 'topicmodel_tests', 'topicmodels.LDA', 'topicmodels.multimix','topicmodels.samplers'],
      package_data={'topicmodels': ['*.txt']},
      cmdclass=cmdclass,
      license="LICENSE",
      description = "Python library that performs Latent Dirichlet Allocation using Gibbs sampling.",
      long_description = open("README.md").read(),
      install_requires=[
          "numpy >= 1.13.3",
          "nltk >= 3.2.4",
          "pandas >= 0.20.3",
          "scipy >= 0.19.1",
          "Cython >= 0.20.1"
      ],
      test_suite = 'topicmodel_tests.my_test_suite'
)
