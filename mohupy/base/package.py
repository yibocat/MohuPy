#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/27 下午7:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from .nums import Fuzznum
from .array import Fuzzarray

from .attributes import report, string
from .function import (isValid, isEmpty, isInitial, convert, qsort, unique,
                       append, remove, pop, reshape, squeeze, clear,
                       ravel, flatten, getmax, getmin, getsum, getprod, mean,
                       fmax, fmin, savez, loadz)

Fuzznum.__repr__ = report
Fuzznum.__str__ = string
Fuzznum.isValid = isValid
Fuzznum.isEmpty = isEmpty
Fuzznum.isInitial = isInitial
Fuzznum.convert = convert
Fuzznum.qsort = qsort
Fuzznum.unique = unique
Fuzznum.append = append
Fuzznum.reshape = reshape
Fuzznum.squeeze = squeeze
Fuzznum.clear = clear
Fuzznum.ravel = ravel
Fuzznum.flatten = flatten
Fuzznum.max = getmax
Fuzznum.min = getmin
Fuzznum.sum = getsum
Fuzznum.prod = getprod
Fuzznum.mean = mean

Fuzzarray.__repr__ = report
Fuzzarray.__str__ = string
Fuzzarray.isValid = isValid
Fuzzarray.isEmpty = isEmpty
Fuzzarray.isInitial = isInitial

Fuzzarray.qsort = qsort
Fuzzarray.unique = unique
Fuzzarray.append = append
Fuzzarray.reshape = reshape
Fuzzarray.squeeze = squeeze
Fuzzarray.clear = clear
Fuzzarray.ravel = ravel
Fuzzarray.flatten = flatten
Fuzzarray.max = getmax
Fuzzarray.min = getmin
Fuzzarray.sum = getsum
Fuzzarray.prod = getprod
Fuzzarray.mean = mean

Fuzzarray.fmax = fmax
Fuzzarray.fmin = fmin
Fuzzarray.remove = remove
Fuzzarray.pop = pop
Fuzzarray.savez = savez
Fuzzarray.loadz = loadz


from .operation import (add, sub, mul, div,
                        pow, equal, inequal,
                        lt, gt, le, ge, matmul, getitem)

Fuzznum.__add__ = add
Fuzznum.__radd__ = add
Fuzznum.__sub__ = sub
Fuzznum.__mul__ = mul
Fuzznum.__rmul__ = mul
Fuzznum.__truediv__ = div
Fuzznum.__pow__ = pow
Fuzznum.__eq__ = equal
Fuzznum.__ne__ = inequal
Fuzznum.__lt__ = lt
Fuzznum.__gt__ = gt
Fuzznum.__le__ = le
Fuzznum.__ge__ = ge

Fuzzarray.__add__ = add
Fuzzarray.__radd__ = add
Fuzzarray.__sub__ = sub
Fuzzarray.__mul__ = mul
Fuzzarray.__rmul__ = mul
Fuzzarray.__truediv__ = div
Fuzzarray.__pow__ = pow
Fuzzarray.__eq__ = equal
Fuzzarray.__ne__ = inequal
Fuzzarray.__lt__ = lt
Fuzzarray.__gt__ = gt
Fuzzarray.__le__ = le
Fuzzarray.__ge__ = ge
Fuzzarray.__matmul__ = matmul
Fuzzarray.__getitem__ = getitem
