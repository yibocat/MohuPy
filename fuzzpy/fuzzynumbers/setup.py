# from setuptools import setup, Extension
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy

include_dirs = [numpy.get_include()]

ext = [
    Extension("fuzzpy.fuzzynumbers.qrungifn.qrungifn",
              ["fuzzpy/fuzzynumbers/qrungifn/qrungifn.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
    Extension("fuzzpy.fuzzynumbers.qrungifn.fuzzymath",
              ["fuzzpy/fuzzynumbers/qrungifn/fuzzymath.pyx"]),

    Extension("fuzzpy.fuzzynumbers.qrungivfn.qrungivfn",
              ["fuzzpy/fuzzynumbers/qrungivfn/qrungivfn.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
    Extension("fuzzpy.fuzzynumbers.qrungivfn.fuzzymath",
              ["fuzzpy/fuzzynumbers/qrungivfn/fuzzymath.pyx"]),

    Extension("fuzzpy.fuzzynumbers.qrungdhfe.qrungdhfe",
              ["fuzzpy/fuzzynumbers/qrungdhfe/qrungdhfe.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
    Extension("fuzzpy.fuzzynumbers.qrungdhfe.fuzzymath",
              ["fuzzpy/fuzzynumbers/qrungdhfe/fuzzymath.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),

    Extension("fuzzpy.fuzzynumbers.__fuzzmath",
              ["fuzzpy/fuzzynumbers/__fuzzmath.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
    Extension('fuzzpy.fuzzynumbers.fuzzmath',
              ['fuzzpy/fuzzynumbers/fuzzmath.pyx']),

    Extension("fuzzpy.fuzzynumbers.Fuzzynum",
              ["fuzzpy/fuzzynumbers/Fuzzynum.pyx"]),
    Extension("fuzzpy.fuzzynumbers.archimedean",
              ["fuzzpy/fuzzynumbers/archimedean.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])
]

setup(name='fuzzpy',
      ext_modules=cythonize(ext, language_level=3, ))
