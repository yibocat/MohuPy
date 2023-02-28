#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

from setuptools import Extension, setup, find_packages
from mohusets.configuration import *
import numpy

include_dirs = [numpy.get_include()]

import os.path


def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in ('.pyx', '.py'):
                if extension.language == 'c++':
                    ext = '.cpp'
                else:
                    ext = '.c'
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions


USE_CYTHON = False  # command line option, try-import, ...
ext = '.pyx' if USE_CYTHON else '.c'
# ext = '.pyx'

ext1 = Extension("mohusets.fuzzysets.__fsmath",
                 ["./mohusets/fuzzysets/__fsmath" + ext],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext2 = Extension("mohusets.fuzzysets.fsmath",
                 ["./mohusets/fuzzysets/fsmath" + ext],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext3 = Extension("mohusets.fuzzynumbers.qifn.fuzzy_element",
                 ["./mohusets/fuzzynumbers/qifn/fuzzy_element" + ext],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])
ext4 = Extension("mohusets.fuzzynumbers.qifn.fuzzymath",
                 ["./mohusets/fuzzynumbers/qifn/fuzzymath" + ext])

ext5 = Extension("mohusets.fuzzynumbers.qivfn.fuzzy_element",
                 ["./mohusets/fuzzynumbers/qivfn/fuzzy_element" + ext],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext6 = Extension("mohusets.fuzzynumbers.qivfn.fuzzymath",
                 ["./mohusets/fuzzynumbers/qivfn/fuzzymath" + ext])

ext7 = Extension("mohusets.fuzzynumbers.qdhfe.fuzzy_element",
                 ["./mohusets/fuzzynumbers/qdhfe/fuzzy_element" + ext],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext8 = Extension("mohusets.fuzzynumbers.qdhfe.fuzzymath",
                 ["./mohusets/fuzzynumbers/qdhfe/fuzzymath" + ext],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext9 = Extension("mohusets.fuzzynumbers.__fuzzmath",
                 ["./mohusets/fuzzynumbers/__fuzzmath" + ext],
                 include_dirs=include_dirs,
                 define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

ext10 = Extension("mohusets.fuzzynumbers.Fuzzynum",
                  ["./mohusets/fuzzynumbers/Fuzzynum" + ext])

ext11 = Extension("mohusets.fuzzynumbers.archimedean",
                  ["./mohusets/fuzzynumbers/archimedean" + ext],
                  include_dirs=include_dirs,
                  define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])

extensions = [ext1, ext2, ext3, ext4, ext5, ext6, ext7, ext8, ext9, ext10, ext11]

if USE_CYTHON:
    from Cython.Build import cythonize

    extensions = cythonize(extensions, language_level=3)

else:
    extensions = no_cythonize(extensions, language_level=3)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=about['name'],
    # ext_modules=no_cythonize(extensions, language_level=3),
    ext_modules=extensions,
    zip_safe=False,
    packages=find_packages(),
    description=about['description'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=about['version'],
    author=about['author'],
    author_email=about['email'],
    url=about['url'],
    license=about['license'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=install_requires,
)
