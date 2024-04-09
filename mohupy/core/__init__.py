#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 上午11:47
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

__all__ = []

from .base import FuzzType
from .fuzzarray import Fuzzarray
from .fuzznums import Fuzznum

from .regedit import Registry
from .operationpackage import *
from .operationLib import archimedeanDict

__all__ += ['FuzzType', 'Fuzzarray', 'Fuzznum',
            'Registry', 'archimedeanDict']

# from .function import (valid, empty, initial, convert, qsort, unique,
#                        append, remove, pop, reshape, squeeze, clear,
#                        ravel, flatten, getmax, getmin, getsum,getprod,
#                        mean, fmax, fmin)
# from .operation import (add, sub, mul, div, pow, matmul, equal, inequal,
#                         lt, gt, le, ge, getitem)

# __all__ += [
#     'valid', 'empty', 'initial', 'convert', 'qsort', 'unique',
#     'append', 'remove', 'pop', 'reshape', 'squeeze', 'clear',
#     'ravel', 'flatten', 'getmax', 'getmin', 'getsum', 'getprod', 'mean',
#     'fmax', 'fmin',
#     'add', 'sub', 'mul', 'div', 'pow', 'matmul', 'equal', 'inequal',
#     'lt', 'gt', 'le', 'ge', 'getitem'
# ]

from .construct import fuzznum, fuzzset
__all__ += ['fuzznum', 'fuzzset']

from .constant import Approx
__all__ += ['Approx']
