#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/26 下午2:47
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
__all__ = []

from .nums import Fuzznum
from .array import Fuzzarray
from .base import FuzzType

from .function import normalize, broadcast_to
from .regedit import Registry
from .package import *

__all__ += ['FuzzType',
            'Fuzznum',
            'Fuzzarray',
            'normalize',
            'Registry',
            'broadcast_to']

from .function import (isValid, isEmpty, isInitial, convert, qsort, unique,
                       append, remove, pop, reshape, squeeze, clear,
                       ravel, flatten, getmax, getmin, getsum, getprod, mean,
                       fmax, fmin)
from .operation import (add, sub, mul, div, pow, matmul, equal, inequal,
                        lt, gt, le, ge, getitem)

__all__ += [
    'isValid', 'isEmpty', 'isInitial', 'convert', 'qsort', 'unique',
    'append', 'remove', 'pop', 'reshape', 'squeeze', 'clear',
    'ravel', 'flatten', 'getmax', 'getmin', 'getsum', 'getprod', 'mean',
    'fmax', 'fmin',
    'add', 'sub', 'mul', 'div', 'pow', 'matmul', 'equal', 'inequal',
    'lt', 'gt', 'le', 'ge', 'getitem'
]

from .fuzzfunc import fuzznum, fuzzset

__all__ += ['fuzznum', 'fuzzset']
