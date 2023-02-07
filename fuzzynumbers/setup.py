from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy

include_dirs = [numpy.get_include()]

ext = [
    Extension("fuzzynumbers.qrungifn.qrungifn",
              ["fuzzynumbers/qrungifn/qrungifn.pyx"],
              include_dirs=include_dirs),
    Extension("fuzzynumbers.qrungifn.fuzzymath",
              ["fuzzynumbers/qrungifn/fuzzymath.pyx"]),
    Extension("fuzzynumbers.qrungivfn.qrungivfn",
              ["fuzzynumbers/qrungivfn/qrungivfn.pyx"],
              include_dirs=include_dirs),
    Extension("fuzzynumbers.qrungivfn.fuzzymath",
              ["fuzzynumbers/qrungivfn/fuzzymath.pyx"]),
    Extension("fuzzynumbers.qrungdhfe.qrungdhfe",
              ["fuzzynumbers/qrungdhfe/qrungdhfe.pyx"],
              include_dirs=include_dirs),
    Extension("fuzzynumbers.qrungdhfe.fuzzymath",
              ["fuzzynumbers/qrungdhfe/fuzzymath.pyx"],
              include_dirs=include_dirs),
    Extension("fuzzynumbers.Fuzzynum",
              ["fuzzynumbers/Fuzzynum.pyx"]),
    Extension("fuzzynumbers.archimedean",
              ["fuzzynumbers/archimedean.pyx"],
              include_dirs=include_dirs)]

setup(name='qrungifn',
      ext_modules=cythonize(ext, language_level=3))
