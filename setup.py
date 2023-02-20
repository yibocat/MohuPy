#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/20 下午10:06
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzPy

from setuptools import Extension, setup, find_packages

import numpy

include_dirs = [numpy.get_include()]

USE_CYTHON = ...  # command line option, try-import, ...

ext = '.pyx' if USE_CYTHON else '.c'
ext1 = Extension("fuzzpy.fuzzysets.__fsmath",
                 ["fuzzpy/fuzzysets/__fsmath.pyx"],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext2 = Extension("fuzzpy.fuzzysets.fsmath",
                 ["fuzzpy/fuzzysets/fsmath.pyx"],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext3 = Extension("fuzzpy.fuzzynumbers.qrungifn.qrungifn",
                 ["fuzzpy/fuzzynumbers/qrungifn/qrungifn.pyx"],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])
ext4 = Extension("fuzzpy.fuzzynumbers.qrungifn.fuzzymath",
                 ["fuzzpy/fuzzynumbers/qrungifn/fuzzymath.pyx"])

ext5 = Extension("fuzzpy.fuzzynumbers.qrungivfn.qrungivfn",
                 ["fuzzpy/fuzzynumbers/qrungivfn/qrungivfn.pyx"],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext6 = Extension("fuzzpy.fuzzynumbers.qrungivfn.fuzzymath",
                 ["fuzzpy/fuzzynumbers/qrungivfn/fuzzymath.pyx"])

ext7 = Extension("fuzzpy.fuzzynumbers.qrungdhfe.qrungdhfe",
                 ["fuzzpy/fuzzynumbers/qrungdhfe/qrungdhfe.pyx"],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext8 = Extension("fuzzpy.fuzzynumbers.qrungdhfe.fuzzymath",
                 ["fuzzpy/fuzzynumbers/qrungdhfe/fuzzymath.pyx"],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext9 = Extension("fuzzpy.fuzzynumbers.__fuzzmath",
                 ["fuzzpy/fuzzynumbers/__fuzzmath.pyx"],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext10 = Extension("fuzzpy.fuzzynumbers.Fuzzynum",
                  ["fuzzpy/fuzzynumbers/Fuzzynum.pyx"])

ext11 = Extension("fuzzpy.fuzzynumbers.archimedean",
                  ["fuzzpy/fuzzynumbers/archimedean.pyx"],
                  include_dirs=include_dirs,
                  define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

extensions = [ext1, ext2, ext3, ext4, ext5, ext6, ext7, ext8, ext9, ext10, ext11]

if USE_CYTHON:
    from Cython.Build import cythonize

    extensions = cythonize(extensions, language_level=3)

setup(
    name="sci-fuzzpy",
    version="0.0.1",
    ext_modules=cythonize(extensions, language_level=3),
    packages=find_packages(),
    zip_safe=False,
)
