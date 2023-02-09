# from setuptools import setup, Extension
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy
import os
root = os.getcwd()
include_dirs = [numpy.get_include()]

ext = [
    Extension("fuzzynumbers.qrungifn.qrungifn",
              [root+"/fuzzynumbers/qrungifn/qrungifn.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
    Extension("fuzzynumbers.qrungifn.fuzzymath",
              [root+"/fuzzynumbers/qrungifn/fuzzymath.pyx"]),

    Extension("fuzzynumbers.qrungivfn.qrungivfn",
              [root+"/fuzzynumbers/qrungivfn/qrungivfn.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
    Extension("fuzzynumbers.qrungivfn.fuzzymath",
              [root+"/fuzzynumbers/qrungivfn/fuzzymath.pyx"]),

    Extension("fuzzynumbers.qrungdhfe.qrungdhfe",
              [root+"/fuzzynumbers/qrungdhfe/qrungdhfe.pyx"],
              include_dirs=include_dirs),
    Extension("fuzzynumbers.qrungdhfe.fuzzymath",
              [root+"/fuzzynumbers/qrungdhfe/fuzzymath.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),

    Extension("fuzzynumbers.__fuzzmath",
              [root+"/fuzzynumbers/__fuzzmath.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
    Extension('fuzzynumbers.fuzzmath',
              [root+'/fuzzynumbers/fuzzmath.pyx']),

    Extension("fuzzynumbers.Fuzzynum",
              [root+"/fuzzynumbers/Fuzzynum.pyx"]),
    Extension("fuzzynumbers.archimedean",
              [root+"/fuzzynumbers/archimedean.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])
]

setup(name='fuzzpy',
      ext_modules=cythonize(ext, language_level=3, ))
