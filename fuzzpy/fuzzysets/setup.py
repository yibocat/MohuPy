
#  Copyright (C) yibocat 2023 all Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/17 下午4:43
#  Author: yibow
#  E-mail: yibocat@yeah.net
#  Software: fuzzpy

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy
include_dirs = [numpy.get_include()]

ext = [
    Extension("fuzzysets.__fsmath",
              ["fuzzysets/__fsmath.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),

    Extension("fuzzysets.fsmath",
              ["fuzzysets/fsmath.pyx"],
              include_dirs=include_dirs,
              define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
]

setup(
    name="fuzzysets",
    ext_modules=cythonize(ext, language_level=3))
