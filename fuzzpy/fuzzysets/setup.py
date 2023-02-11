
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy
include_dirs = [numpy.get_include()]

ext = [
    Extension("fuzzpy.fuzzysets.__fsmath",
              ["fuzzpy/fuzzysets/__fsmath.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),

    Extension("fuzzpy.fuzzysets.fsmath",
              ["fuzzpy/fuzzysets/fsmath.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
]

setup(
    name="fuzzysets",
    ext_modules=cythonize(ext, language_level=3))
